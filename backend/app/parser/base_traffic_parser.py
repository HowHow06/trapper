import json
import re
from urllib import parse

from app.core.http_util import ContentType, HttpMethod


class BaseTrafficParser:

    DEAFAULT_PARSER = "raw"
    CHROME_PARSER = "chrome-plugin"

    DIGITAL = (1, 'trapper_int')
    LETTER = (2, 'trapper_str')
    DIGMIXEDLETER = (3, 'trapper_mix')
    OTHER = (4, 'trapper_other')
    FLOAT = (5, 'trapper_float')

    """
    Traffic parser, the traffic obtained from the Chrome plugin is not quite the same as the traffic obtained from HTTP requests
    """

    @staticmethod
    def _parse_get_parameter(url):
        """
        Parse http get request parameters
        :return: 
        """
        result = dict()
        temp_keys_value = re.findall(
            u'\?((?:\w*=[\s\S\u4e00-\u9fa5]*&?)*)', url, re.S)
        if len(temp_keys_value) > 0:
            temp_keys_value = temp_keys_value[0]
            keys = re.findall('(\w{1,})=', temp_keys_value, re.S)
            for key in keys:
                regular = u'{}=([\s\S\u4e00-\u9fa5][^&^\n]*)'.format(key)
                try:
                    value = re.findall(regular, temp_keys_value)[0]
                except IndexError:
                    value = ""
                result[key] = value
        return result

    @staticmethod
    def _parse_post_parameter(data, content_type):
        """
        Parse post parameters
        :param data: 
        :return: 
        """
        result = dict()
        if not content_type or ContentType.ResourceContentType.DEFAULT in content_type.lower():
            temp_keys_value = re.findall(
                u'\?*((?:\w*=[\s\S\u4e00-\u9fa5]*&?)*)', data, re.S)[0]
        elif ContentType.ResourceContentType.JSON in content_type.lower():
            return json.loads(data)
        elif ContentType.ResourceContentType.XML in content_type.lower():
            return data  # not supported yet
        elif ContentType.ResourceContentType.FORM in content_type.lower():
            filename = re.findall('filename="([\S\s]*)"', data, re.S)[0]
            return {'filename': filename}
        if len(temp_keys_value) > 0:
            keys = re.findall('(\w{1,})=', temp_keys_value, re.S)
            for key in keys:
                regular = u'{}=([\s\S\u4e00-\u9fa5][^&^\n]*)'.format(key)
                value = re.findall(regular, temp_keys_value)[0]
                result[key] = value
        return result

    @staticmethod
    def get_parameter(url, data=None, http_method=HttpMethod.GET, content_type=None):
        """
        Parse parameters
        """

        if http_method and http_method.lower() == HttpMethod.GET:
            return BaseTrafficParser._parse_get_parameter(url)
        elif http_method and http_method.lower() == HttpMethod.POST and data:
            return BaseTrafficParser._parse_post_parameter(data, content_type)

    @staticmethod
    def _replace_param_val_to_identification(http_parameter):
        """
        Replace parameters value to trapper_int e.g.
        :param http_parameter: 
        :return: 
        """
        result = {}
        for key, value in http_parameter.items():
            result[key] = value if key == "submit" else BaseTrafficParser._replace_identification(
                value)
        return result

    @staticmethod
    def simplify_request(url, data=None, http_method=HttpMethod.GET, content_type=None):
        """
        Parse request，extract additional information like method, url, content type
        :param url: 
        :param data: 
        :param http_method: 
        :param content_type: 
        :return: 
        """
        if (http_method and http_method.lower() == HttpMethod.GET) or content_type is None:
            return {"url": BaseTrafficParser._simplify_get_request(url), "data": data, "http_method": http_method,
                    "content_type": None}
        elif http_method and http_method.lower() == HttpMethod.POST:
            if ContentType.ResourceContentType.DEFAULT in content_type:
                return {"url": url, "data": BaseTrafficParser._simplify_post_request_default(data),
                        "http_method": http_method, "content_type": ContentType.ResourceContentType.DEFAULT}
            elif ContentType.ResourceContentType.JSON in content_type:
                return {"url": url, "data": json.dumps(BaseTrafficParser._simplify_post_request_json(data)),
                        "http_method": http_method, "content_type": ContentType.ResourceContentType.JSON}
            elif ContentType.ResourceContentType.XML in content_type:
                return {"url": url, "data": data, "http_method": http_method,
                        "content_type": ContentType.ResourceContentType.XML}
            elif ContentType.ResourceContentType.FORM in content_type:
                return {"url": url, "data": BaseTrafficParser._simplify_post_request_form(data),
                        "http_method": http_method, "content_type": ContentType.ResourceContentType.FORM}
            elif ContentType.ResourceContentType.TXT in content_type:
                return {"url": url, "data": data, "http_method": http_method,
                        "content_type": ContentType.ResourceContentType.TXT}

    @staticmethod
    def _simplify_get_request(url):
        """
        Parse get request
        :param data: 
        :param http_method: 
        :param content_type: 
        :return: 
        """
        have_parameter = False
        result_urls_key = None
        result_parameter = ""
        http_parameter = BaseTrafficParser._parse_get_parameter(url)
        http_parameter = BaseTrafficParser._replace_param_val_to_identification(
            http_parameter)
        for key, value in http_parameter.items():
            result_parameter += "{}={}&".format(key, value)
            have_parameter = True
        if have_parameter:
            result_parameter = "?{}".format(result_parameter[:-1])
            result_urls_key = re.subn(
                u'\?((?:\w*=[\s\S\u4e00-\u9fa5]*&?)*)', result_parameter, url)[0]
        return result_urls_key if result_urls_key else url

    @staticmethod
    def _simplify_post_request_default(data):
        """
        Parse application/x-www-form-urlencoded content type
        :param data: 
        :param http_method: 
        :param content_type: 
        :return: 
        """
        result_urls_key = None
        have_parameter = False
        result_parameter = ""
        http_parameter = BaseTrafficParser._parse_post_parameter(
            data, ContentType.ResourceContentType.DEFAULT)
        http_parameter = BaseTrafficParser._replace_param_val_to_identification(
            http_parameter)
        for key, value in http_parameter.items():
            result_parameter += "{}={}&".format(key, value)
            have_parameter = True
        if have_parameter:
            result_urls_key = result_parameter[:-1]
        return result_urls_key if result_urls_key else data

    @staticmethod
    def _simplify_post_request_json(data):
        """
        Parse application/json content type
        :param data: 
        :return: 
        """
        return BaseTrafficParser._get_json_parameter(data)

    @staticmethod
    def _simplify_post_request_form(data):
        """
        Parse multipart/form-data; boundary=----WebKitFormBoundaryH0TGOzR6zJhOJSVB
        :return: 
        """
        result_parameter = ""
        identification_result_parameter = None
        http_parameter = BaseTrafficParser._parse_post_parameter(
            data, ContentType.ResourceContentType.FORM)
        for key, value in http_parameter.items():
            result_parameter += '{}="{}"'.format(key, value)
        http_parameter = BaseTrafficParser._replace_param_val_to_identification(
            http_parameter)
        for key, value in http_parameter.items():
            identification_result_parameter = ""
            identification_result_parameter += '{}="{}"'.format(key, value)
        if result_parameter.strip() != "" and identification_result_parameter:
            data = str(data).replace(result_parameter,
                                     identification_result_parameter)
        return data

    def _simplify_post_request(url, data, http_method, content_type):
        """
        Parse post request
        :param data: 
        :param http_method: 
        :param content_type: 
        :return: 
        """
        result_parameter = None
        http_parameter = BaseTrafficParser.get_parameter(
            url, data, http_method, content_type)
        http_parameter = BaseTrafficParser.replace_param_val_to_identification(
            http_parameter)
        for key, value in http_parameter.items():
            result_parameter += "{}={}&".format(key, value)
            have_parameter = True
        if have_parameter:
            result_parameter = "?{}".format(result_parameter[:-1])
            result_urls_key = re.subn(
                u'\?((?:\w*=[\s\S\u4e00-\u9fa5]*&?)*)', result_parameter, url)[0]
        return result_urls_key if result_urls_key else url

    @staticmethod
    def _get_json_parameter(str):
        """
        str1 = '{"name":{"pass": {"bb": 12222, "aa": {"hello": "xxx"}}}, "hello": "ssss"}'
        str2 = ```
        {"video":{"id":"29BA6ACE7A9427489C33DC5901307461","title":"class01","desp":"","tags":" ","duration":503,"category":"07AD1E11DBE6FDFC","image":"http://2.img.bokecc.com/comimage/0DD1F081022C163E/2016-03-09/29BA6ACE7A9427489C33DC5901307461-0.jpg","imageindex":0,"image-alternate":[{"index":0,"url":"http://2.img.bokecc.com/comimage/0DD1F081022C163E/2016-03-09/29BA6ACE7A9427489C33DC5901307461-0/0.jpg"},{"index":1,"url":"http://2.img.bokecc.com/comimage/0DD1F081022C163E/2016-03-09/29BA6ACE7A9427489C33DC5901307461-0/1.jpg"},{"index":2,"url":"http://2.img.bokecc.com/comimage/0DD1F081022C163E/2016-03-09/29BA6ACE7A9427489C33DC5901307461-0/2.jpg"},{"index":3,"url":"http://2.img.bokecc.com/comimage/0DD1F081022C163E/2016-03-09/29BA6ACE7A9427489C33DC5901307461-0/3.jpg"}]}}
        ```
        str3 = '{"name":{"pass": [{"bb":"xxx", "aaa": "bb"}, {"bb":"xxx34444444", "aaa": "bb"}]}, "hello": "ssss"}'
        str = '{"name":[{"bb":"xxx"}]}'
        str4 = '{"name":"chenming","whoamo":"11123333"}'
        Parse JSON with recursive
        :param str: 
        :return: 
        """
        result = {}
        temp_jsons = BaseTrafficParser.loads(str)
        if temp_jsons is not None:
            if isinstance(temp_jsons, list):
                temp_result = dict()
                temp_result_list = list()
                for temp_json in temp_jsons:
                    BaseTrafficParser.set_type(temp_result, temp_json)
                    temp_result_list.append(temp_result)
                return temp_result_list
            else:
                BaseTrafficParser._set_type(result, temp_jsons)
                return result
        return result

    @staticmethod
    def _set_type(result, temp_json):
        """
        mainly called by get_json_parameter
        :param result: 
        :param temp_json: 
        :return: 
        """
        for key, value in temp_json.items():
            if BaseTrafficParser.loads(value) is not None:
                result[key] = BaseTrafficParser._get_json_parameter(value)
            else:
                result[key] = BaseTrafficParser._replace_identification(value)

    @staticmethod
    def loads(object):
        result = None
        if isinstance(object, dict) or isinstance(object, list):
            return object
        try:
            result = json.loads(object)
            int(result)
            result = None
        except Exception as e:
            pass
        finally:
            return result

    @staticmethod
    def check_type(value):
        value = str(value)
        if sum([n.isdigit() for n in value.strip().split('.')]) == 2:
            return BaseTrafficParser.FLOAT[0]
        if value.isdigit():
            return BaseTrafficParser.DIGITAL[0]
        elif value.isalpha():
            return BaseTrafficParser.LETTER[0]
        elif value.isalnum():
            return BaseTrafficParser.DIGMIXEDLETER[0]
        else:
            return BaseTrafficParser.OTHER[0]

    @staticmethod
    def surround_with_single_quote(value):
        if str(value).startswith("'") and str(value).endswith("'"):
            return True, value[1:-1]
        else:
            return False, value

    @staticmethod
    def _replace_identification(value):
        is_surround_with_single_quote, value = BaseTrafficParser.surround_with_single_quote(
            value)
        value_type = None
        try:
            value_type = BaseTrafficParser.check_type(parse.quote(value))
        except TypeError:
            value_type = BaseTrafficParser.check_type(value)

        if value_type == BaseTrafficParser.DIGITAL[0]:
            value = BaseTrafficParser.remove_int_same()
        elif value_type == BaseTrafficParser.LETTER[0]:
            value = BaseTrafficParser.remove_str_same()
        elif value_type == BaseTrafficParser.DIGMIXEDLETER[0]:
            value = BaseTrafficParser.remove_mix_same()
        elif value_type == BaseTrafficParser.FLOAT[0]:
            value = BaseTrafficParser.remove_float_same()
        else:
            value = BaseTrafficParser.remove_other_same()
        if is_surround_with_single_quote:
            value = "'{}'".format(value)
        return value

    @staticmethod
    def remove_int_same():
        return BaseTrafficParser.DIGITAL[1]

    @staticmethod
    def remove_str_same():
        return BaseTrafficParser.LETTER[1]

    @staticmethod
    def remove_mix_same():
        return BaseTrafficParser.DIGMIXEDLETER[1]

    @staticmethod
    def remove_other_same():
        return BaseTrafficParser.OTHER[1]

    @staticmethod
    def remove_float_same():
        return BaseTrafficParser.FLOAT[1]

    @staticmethod
    def replace(str, substr):
        """
        :param old_str: 
        :param new_str: 
        :return: 
        """
        if isinstance(str, dict):
            str = json.dumps(str)
        return str.replace(BaseTrafficParser.DIGITAL[1], substr).replace(BaseTrafficParser.LETTER[1], substr).replace(
            BaseTrafficParser.DIGMIXEDLETER[1], substr).replace(BaseTrafficParser.OTHER[1], substr).replace(
            BaseTrafficParser.FLOAT[1], substr)

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
            poc_result = BaseTrafficParser.simplify_request(url=url, data=data, http_method=http_method,
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
