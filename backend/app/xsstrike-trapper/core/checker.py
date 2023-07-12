import copy
import re
from urllib.parse import unquote

from core.config import xsschecker
from core.requester import requester
from core.utils import fillHoles, fillHoles2, replaceValue
from fuzzywuzzy import fuzz


def checker(url, params, headers, GET, delay, payload, positions, timeout, encoding, previousReflections=[]):
    checkString = 'st4r7s' + payload + '3nd'
    if encoding:
        checkString = encoding(unquote(checkString))
    response = requester(url, replaceValue(
        params, xsschecker, checkString, copy.deepcopy), headers, GET, delay, timeout).text.lower()
    reflectedPositions = []
    for match in re.finditer('st4r7s', response):
        reflectedPositions.append(match.start())
    # TRAPPER: Only call fillHoles if there are missing or extra reflected positions
    if len(reflectedPositions) != len(positions):
        filledPositions = fillHoles2(positions, reflectedPositions)
    else:
        # No need to fill holes, reflectedPositions matches expected positions
        filledPositions = list(reflectedPositions)
    # Itretating over the reflections
    num = 0
    efficiencies = []
    for position in filledPositions:
        allEfficiencies = []
        # TRAPPER: removed the part where it uses the reflectedPositions, which does not make sense
        if position:
            reflected = response[position:position+len(checkString)]
            if encoding:
                checkString = encoding(checkString.lower())
            # TRAPPER: added `.lower()` here
            efficiency = fuzz.partial_ratio(
                reflected.lower(), checkString.lower())
            if reflected[:-2] == ('\\%s' % checkString.replace('st4r7s', '').replace('3nd', '')):
                efficiency = 90
            allEfficiencies.append(efficiency)
            efficiencies.append(max(allEfficiencies))
        else:
            efficiencies.append(0)
        num += 1
    # TRAPPER: removed the part where it removes empty values
    previousReflections.clear()
    previousReflections.extend(reflectedPositions)
    return list(efficiencies)
