import json
import re
from sys import version_info

import requests

if version_info < (3, 0):
    from urllib import quote
else:
    from urllib.parse import quote

__all__ = ["is_uploadordownload", "remove_http", "get_host_port", "get_host_port_protocol", "get_top_domain",
           "header_to_lowercase",
           "url_encode", "get_parent_route", "get_parent_route"]


DEFAULT_TIMEOUT = 10
DEFAULT_CHUNK_SIZE = 512


def is_uploadordownload(package):
    """
    Determine whether it's an upload type
    :param package: 
    :return: 
    """
    if package["data"] and "headers" in package["data"]:
        headers = json.loads(package["data"]["headers"])
        if "Content-Type" in headers:
            if ContentType.StaticResourceContentType.UPLOAD_FORM in headers["Content-Type"] or \
                    ContentType.StaticResourceContentType.DOWNLOAD in headers["Content-Type"]:
                return True
        if "content-type" in headers:  # 来自插件的请求
            if ContentType.StaticResourceContentType.UPLOAD_FORM in headers["content-type"] or \
                    ContentType.StaticResourceContentType.DOWNLOAD in headers["content-type"]:
                return True
    return False


def download_file(url, save_fp, timeout=DEFAULT_TIMEOUT, chunk_size=DEFAULT_CHUNK_SIZE):
    req = requests.get(url, stream=True, timeout=timeout)
    with open(save_fp, "wb") as file:
        for chunk in req.iter_content(chunk_size=chunk_size):
            if chunk:
                file.write(chunk)


def remove_http(url):
    """
    1. First, determine whether it starts with http or https
    Extract the hostname from http://xxxx/
    :return: 
    """
    domain = re.findall(r'(?:http[s]?://)?([\w\.\-]*)/*', url)
    if len(domain) > 0:
        host = str(domain[0]).replace("/", "")
    else:
        host = url.replace("/", "")
    return host


def get_host_port(url, default_port=80):
    """
    Extract domain name and port from the url, for example, http://xxxx:8090
    :param url: 
    :return: 
    """
    host_port = re.findall(r'(?:http[s]?://)?([\w\.-]*)[:]?(\d*)/*', url)
    if len(host_port) > 0:
        host, port = host_port[0][0], default_port if host_port[0][1] == '' else int(
            host_port[0][1])
    else:
        host = url, port = 80
    return host, port


def get_host_port_protocol(url, default_port=80):
    """
    Extract host, port, protocol
    :param url: 
    :param default_port: 
    :return: 
    """
    host, port = get_host_port(url)
    if str(url).startswith("https://"):
        protocol = "https"
    else:
        protocol = "http"
    return host, port, protocol


def get_top_domain(url):
    """
    Obtain the top-level domain from the url
    :param url: 
    :return: 
    """
    sub_domain = remove_http(url)
    return sub_domain if len(sub_domain.split(".")) == 2 else ".".join(sub_domain.split(".")[-2:])


def header_to_lowercase(headers):
    """
    :param header: 
    :return: 
    """
    result = dict()
    for key in headers.keys():
        if key.lower() == "content-type":
            result['content-type'] = headers[key]
        result[key] = headers[key]
    return result


def url_encode(str):
    return quote(str).replace("/", "%2F")


def get_parent_route(url):
    """
    Get the parent route
    :param url: 
    :return: 
    """
    parameter = re.split(r'/[^/]*$', url, re.S)
    try:
        result = parameter[0] + "/"
    except IndexError:
        result = url + "/"
    if result == "https://" or result == "http://":
        result = url + "/"
    return result


class ContentType:
    NAME = "Content-Type"

    class ResourceContentType:
        # static resource type
        PNG = "image/png"
        TIF = "image/tiff"
        FAX = "image/fax"
        GIF = "image/gif"
        ICO = "image/x-icon"
        JPE = "image/jpeg"
        JPEG = "image/jpeg"
        PNG = "image/png"
        WBMP = "image/vnd.wap.wbmp"
        CSS = "text/css"
        MP2 = "audio/mp2"
        MP3 = "audio/mp3"
        MPA = "video/x-mpg"
        MPE = "video/x-mpeg"
        MPG = "video/mpg"
        MP2V = "video/mpeg"
        MP4 = "video/mpeg4"
        MPEG = "video/mpg"
        MPS = "video/x-mpeg"
        WMZ = "video/x-ms-wmv"
        WRM = "video/x-ms-wm"
        WMX = "video/x-ms-wmx"
        WVX = "video/x-ms-wvx"
        # non-static resource type
        UPLOAD_FORM = "multipart/form-data; boundary="
        DOWNLOAD = "application/octet-stream"
        JSON = "application/json"
        XML = "text/xml"
        DEFAULT = "application/x-www-form-urlencoded"
        HTML = "text/html"
        FORM = "multipart/form-data"
        TXT = "text/plain"

        static_resource_list = [PNG, TIF, FAX, GIF, ICO, JPE, JPEG, PNG, WBMP, CSS, MP2, MP3, MPA, MPE, MPG, MP2V, MP4,
                                MPEG, MPS, WMZ, WRM, WMX, WVX]


class StatusCode:
    """
    Response status code
    """
    HTTP_OK = 200
    HTTP_CREATED = 201
    HTTP_NO_CONTENT = 204
    HTTP_BAD_REQUEST = 400
    HTTP_UNAUTHORIZED = 401
    HTTP_FORBIDDEN = 403
    HTTP_NOT_FOUND = 404
    HTTP_METHOD_NOT_ALLOWED = 405
    HTTP_CONFLICT = 409
    HTTP_UNSUPPORTED_MEDIA_TYPE = 415
    HTTP_INTERNAL_SERVER_ERROR = 500
    HTTP_BAD_GATEWAY = 502,
    HTTP_SERVICE_UNAVAILABLE = 503


class UserAgent:
    NAME = "Content-Type"

    class MobileDevices:
        """
        Mobile UA
        """
        ANDROID = "Dalvik/2.1.0 (Linux; U; Android 5.1; OPPO R9m Build/LMY47I)"

    class PCDevices:
        """
        PC UA
        """
        CHROME_MAC = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) " \
                     "Chrome/65.0.33 25.181 Safari/537.36"


class AcceptCharset():
    UTF8 = "UTF-8"


class HttpMethod():
    GET = "get"
    POST = "post"


def json_to_urlencoded(data):
    """
    convert {'B1': 'msghere', 'id': '1', 'msg': 'abc'} to B1=msghere&id=1&msg=abc
    :param json: 
    :return: 
    """
    # import sys
    # reload(sys)
    # sys.setdefaultencoding('utf8')
    result = ""
    for key, value in data.items():
        temp_data = "{}={}".format(key, value)
        result = "{}&{}".format(
            result, temp_data) if result != "" else temp_data
    return result
