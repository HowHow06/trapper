import copy
import re
from urllib.parse import unquote, urlparse

import core.config
from app import crud, schemas
from app.core import constants
from app.db.session import AsyncSessionLocal, get_async_db_url
from core.blindPayloadUtils import PayloadGenerator
from core.checker import checker
from core.colors import end, green, que
from core.config import (minEfficiency, moreReflectedPositionCounterThreshold,
                         xsschecker)
from core.filterChecker import filterChecker
from core.generator import generator
from core.htmlParser import htmlParser
from core.log import setup_logger
from core.requester import requester
from core.trapperDom import dom as trapperDom
from core.utils import getParams, getUrl, getVar, updateVar
from core.wafDetector import wafDetector

payload_generator = PayloadGenerator()
logger = setup_logger(__name__)


async def scan(target, paramData, encoding, headers, delay, timeout, skipDOM, skip, trapper_celery_request_id, trapperBlindXSSRequest):
    async with AsyncSessionLocal() as db:
        GET, POST = (False, True) if paramData else (True, False)
        # If the user hasn't supplied the root url with http(s), we will handle it
        if not target.startswith('http'):
            try:
                response = requester('https://' + target, {},
                                     headers, GET, delay, timeout)
                target = 'https://' + target
            except:
                target = 'http://' + target
        logger.debug('Scan target: {}'.format(target))
        response = requester(target, {}, headers, GET, delay, timeout).text

        if not skipDOM:
            logger.run('Checking for DOM vulnerabilities')
            highlighted = trapperDom(response)
            if highlighted:
                logger.good('Potentially vulnerable objects found')
                logger.red_line(level='good')
                for line in highlighted:
                    # TRAPPER: will print the vulnerable code in the response html
                    logger.no_format(line, level='good')
                    index = line.find(" ")
                    dom_payload = line[index+1:]  # remove the heading number

                    # store to db
                    dom_result = schemas.ResultCreate(
                        request_id=trapper_celery_request_id,
                        vulnerability_id=constants.Vulnerability.DOM_XSS,
                        # remove color code for terminal
                        payload=re.sub(r'\033\[\d+m', '', dom_payload),
                    )
                    await crud.crud_result.create(db, obj_in=dom_result)

                logger.red_line(level='good')

        host = urlparse(target).netloc  # Extracts host out of the url
        logger.debug('Host to scan: {}'.format(host))
        url = getUrl(target, GET)
        logger.debug('Url to scan: {}'.format(url))
        params = getParams(target, paramData, GET)
        logger.debug_json('Scan parameters:', params)
        logger.info('Scan parameters PARAMS: {} | PARAM DATA: {}'.format(
            params, paramData))
        if not params:
            logger.error('No parameters to test.')
            quit()
        WAF = wafDetector(
            url, {list(params.keys())[0]: xsschecker}, headers, GET, delay, timeout)
        if WAF:
            logger.error('WAF detected: %s%s%s' % (green, WAF, end))
        else:
            logger.good('WAF Status: %sOffline%s' % (green, end))

        # inject trapper blind xss request
        if trapperBlindXSSRequest:
            logger.info('Has trapperBlindXSSRequest!')
            for paramName in params.keys():
                logger.info('Looking to inject: %s' % paramName)
                paramsCopy = copy.deepcopy(params)
                for method_name in dir(PayloadGenerator):
                    # Ignore methods starting with underscore, those are usually private methods or Python built-ins
                    if not method_name.startswith('_'):
                        method = getattr(payload_generator, method_name)
                        if callable(method):
                            blind_payload = trapperBlindXSSRequest.replace(
                                '[request_id]', trapper_celery_request_id).replace(
                                '[payload_type]', method_name)
                            blind_payload = method(blind_payload)
                            paramsCopy[paramName] = blind_payload
                            logger.info(
                                'Injecting the URL %s with "%s" payload' % (url, method_name))
                            requester(url, paramsCopy, headers,
                                      GET, delay, timeout)

        latestReflectedPositions = []
        for paramName in params.keys():
            isSkipToNextParam = False
            paramsCopy = copy.deepcopy(params)
            logger.info('Testing parameter: %s' % paramName)
            if encoding:
                paramsCopy[paramName] = encoding(xsschecker)
            else:
                paramsCopy[paramName] = xsschecker
            response = requester(url, paramsCopy, headers, GET, delay, timeout)
            occurences = htmlParser(response, encoding)
            positions = occurences.keys()
            logger.debug('Scan occurences: {}'.format(occurences))
            if not occurences:
                logger.error('No reflection found')
                continue
            else:
                logger.info('Reflections found: %i' % len(occurences))

            logger.run('Analysing reflections')
            efficiencies = filterChecker(
                url, paramsCopy, headers, GET, delay, occurences, timeout, encoding)
            logger.debug('Scan efficiencies: {}'.format(efficiencies))
            logger.run('Generating payloads')
            vectors = generator(occurences, response.text)
            total = 0
            for v in vectors.values():
                total += len(v)
            if total == 0:
                logger.error('No vectors were crafted.')
                continue
            logger.info('Payloads generated: %i' % total)
            progress = 0
            for confidence, vects in vectors.items():
                if isSkipToNextParam:
                    break
                for vect in vects:
                    if core.config.globalVariables['path']:
                        vect = vect.replace('/', '%2F')
                    loggerVector = vect
                    progress += 1
                    logger.run('Progress: %i/%i\r' % (progress, total))
                    if not GET:
                        vect = unquote(vect)
                    previousReflectedPositions = copy.deepcopy(
                        latestReflectedPositions)
                    efficiencies = checker(
                        url, paramsCopy, headers, GET, delay, vect, positions, timeout, encoding, previousReflections=latestReflectedPositions)
                    if len(latestReflectedPositions) > len(previousReflectedPositions) and paramName is not None:
                        variableName = "{}:counter".format(paramName)
                        try:
                            moreReflectedPositionCounter = int(
                                getVar(variableName))
                            logger.debug("moreReflectedPositionCounter: {}".format(
                                moreReflectedPositionCounter))
                            updateVar(variableName,
                                      moreReflectedPositionCounter + 1)
                            if moreReflectedPositionCounter > moreReflectedPositionCounterThreshold:
                                logger.info(
                                    "This param is not suitable to test, skipping to next param...")
                                isSkipToNextParam = True
                                break
                        except:
                            logger.debug(
                                "initializing moreReflectedPositionCounter: ")
                            updateVar(variableName, 1)

                    if not efficiencies:
                        for i in range(len(occurences)):
                            efficiencies.append(0)
                    bestEfficiency = max(efficiencies)
                    if bestEfficiency == 100 or (vect[0] == '\\' and bestEfficiency >= 95):
                        logger.red_line()
                        logger.good('Payload: %s' % loggerVector)
                        logger.info('Efficiency: %i' % bestEfficiency)
                        logger.info('Confidence: %i' % confidence)
                        reflected_result = schemas.ResultCreate(
                            request_id=trapper_celery_request_id,
                            vulnerability_id=constants.Vulnerability.REFLECTED_XSS,
                            payload=loggerVector,
                        )
                        # store to db
                        await crud.crud_result.create(db, obj_in=reflected_result)
                        quit()

                        # if not skip:
                        #     choice = input(
                        #         '%s Would you like to continue scanning? [y/N] ' % que).lower()
                        #     if choice != 'y':
                        #         quit()

                    elif bestEfficiency > minEfficiency:
                        logger.red_line()
                        logger.good('Payload: %s' % loggerVector)
                        logger.info('Efficiency: %i' % bestEfficiency)
                        logger.info('Confidence: %i' % confidence)
            logger.no_format('')
