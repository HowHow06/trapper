import json
import re

from app.core.http_util import ContentType, HttpMethod
from app.parser.base_traffic_parser import BaseTrafficParser


class ChromeTrafficParser(BaseTrafficParser):

    @staticmethod
    def get_parameter(url, data, http_method, content_type):
        """
        get is same as BaseTrafficParser
        :param url: 
        :param data: 
        :param http_method: 
        :param content_type: 
        :return: 
        """
        if (http_method and http_method.lower() == HttpMethod.GET) or content_type is None:
            return BaseTrafficParser.get_parameter(url=url, data=data, http_method=http_method,
                                                   content_type=content_type)
        elif http_method and http_method == HttpMethod.POST:
            return ChromeTrafficParser._parse_post_parameter(data, content_type)

    @staticmethod
    def _parse_post_parameter(data, content_type):
        """
        post is not the same as BaseTrafficParser
        :param data: 
        :param content_type: 
        :return: 
        """
        if content_type:
            content_type = content_type.lower()
        if content_type == ContentType.ResourceContentType.DEFAULT or content_type == ContentType.ResourceContentType.JSON:
            # data = "{\"name\":\"admin\",\"password\":\"admin888\"}" //application/x-www-form-urlencoded
            # data = "\"{\\\"username\\\":\\\"admin\\\",\\\"password\\\":\\\"passss\\\"}\"" //application/json
            return json.loads(data)
        elif content_type == ContentType.ResourceContentType.XML:
            # removing " is not supported yet
            data = re.findall(u'"(.*?)"', data, re.S)[0]
            return data
        elif content_type == ContentType.ResourceContentType.FORM:
            filename = re.findall(
                'filename=[\\\]*"([\w\.]*)[\\\]*"', data, re.S)[0]
            return {'filename': filename}

    @staticmethod
    def simplify_request(url, data=None, http_method=HttpMethod.GET, content_type=None):
        if (http_method and http_method.lower() == HttpMethod.GET) or content_type is None:
            return {"url": BaseTrafficParser._simplify_get_request(url), "data": data, "http_method": http_method,
                    "content_type": None}
        elif http_method and http_method.lower() == HttpMethod.POST:
            if ContentType.ResourceContentType.DEFAULT in content_type.lower():
                return {"url": url, "data": ChromeTrafficParser._simplify_post_request_default(data),
                        "http_method": http_method, "content_type": ContentType.ResourceContentType.DEFAULT}
            elif ContentType.ResourceContentType.JSON in content_type.lower():
                return {"url": url, "data": ChromeTrafficParser._get_json_parameter(
                    ChromeTrafficParser._parse_post_parameter(data, content_type)), "http_method": http_method,
                    "content_type": ContentType.ResourceContentType.JSON}
            elif ContentType.ResourceContentType.XML in content_type.lower():
                return {"url": url, "data": ChromeTrafficParser._parse_post_parameter(data, content_type),
                        "http_method": http_method, "content_type": ContentType.ResourceContentType.XML}
            elif ContentType.ResourceContentType.FORM in content_type.lower():
                # 暂时不处理
                return {"url": url, "data": data, "http_method": http_method,
                        "content_type": ContentType.ResourceContentType.FORM}
            elif ContentType.ResourceContentType.TXT in content_type.lower():
                return {"url": url, "data": data, "http_method": http_method,
                        "content_type": ContentType.ResourceContentType.TXT}

    @staticmethod
    def _simplify_post_request_default(data):
        result_urls_key = None
        have_parameter = False
        result_parameter = ""
        http_parameter = BaseTrafficParser._get_json_parameter(data)
        http_parameter = BaseTrafficParser._replace_param_val_to_identification(
            http_parameter)
        for key, value in http_parameter.items():
            result_parameter += "{}={}&".format(key, value)
            have_parameter = True
        if have_parameter:
            result_urls_key = result_parameter[:-1]
        return result_urls_key if result_urls_key else data

    @staticmethod
    def add_poc_data(url, data, http_method, content_type, poc):
        """
        change the original parameter to poc
        :param url: 
        :param http_method: 
        :param content_type: 
        :param poc: 
        :return: 
        """
        try:
            poc_result = ChromeTrafficParser.simplify_request(url=url, data=data, http_method=http_method,
                                                              content_type=content_type)
            if (http_method and http_method.lower() == HttpMethod.GET) or content_type is None:
                poc_result["url"] = BaseTrafficParser.replace(
                    poc_result["url"], poc)
            elif http_method and http_method.lower() == HttpMethod.POST:
                poc_result["data"] = BaseTrafficParser.replace(
                    poc_result["data"], poc)
        except Exception:
            poc_result = {"url": url, "data": data,
                          "http_method": http_method, "content_type": content_type}
        return poc_result

    @staticmethod
    def to_raw(url, data, http_method, content_type):
        """
        convert chrome plugin traffic to raw
        :param url: 
        :param data: 
        :param http_method: 
        :param content_type: 
        :return: 
        """
        if (http_method and http_method.lower() == HttpMethod.GET) or content_type is None:
            return {"url": url, "data": data, "http_method": http_method, "content_type": content_type}
        elif http_method and http_method.lower() == HttpMethod.POST:
            if ContentType.ResourceContentType.DEFAULT in content_type.lower():
                http_parameter = json.loads(data)
                result_parameter = ""
                for key, value in http_parameter.items():
                    result_parameter += "{}={}&".format(key, value)
                return {"url": url, "data": result_parameter, "http_method": http_method, "content_type": content_type}
            elif ContentType.ResourceContentType.JSON in content_type.lower():
                return {"url": url, "data": json.loads(data), "http_method": http_method, "content_type": content_type}
            elif ContentType.ResourceContentType.XML in content_type.lower():
                data = re.findall(u'"(.*?)"', data, re.S)[0]
                return {"url": url, "data": data, "http_method": http_method, "content_type": content_type}
            elif ContentType.ResourceContentType.FORM in content_type.lower():
                return {"url": url, "data": data, "http_method": http_method, "content_type": content_type}
            elif ContentType.ResourceContentType.TXT in content_type.lower():
                return {"url": url, "data": data, "http_method": http_method, "content_type": content_type}
        return {"url": url, "data": data, "http_method": http_method, "content_type": content_type}
