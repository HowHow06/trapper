
import hashlib
import json
from typing import Any

from app.core import http_util
from app.parser.chrome_traffic_parser import ChromeTrafficParser


def get_request_information(request_data) -> dict[str, Any] | None:
    """
    analyse the http request information, e.g. {"url": xxxx, "data": xxx, "http_method": xxx, "content_type": xxx}
    :return: 
    """
    request_data.pop('requestid')

    http_method = str(request_data["method"]).lower()
    url = str(request_data["url"]).strip()
    headers = http_util.header_to_lowercase(
        json.loads(request_data['headers']))
    content_type = None

    if headers is not None and http_util.ContentType.NAME.lower() in headers:
        content_type = headers["content-type"]

    data = request_data['data'] if "data" in request_data else None
    request_information = ChromeTrafficParser.simplify_request(url=url, data=data,
                                                               http_method=http_method,
                                                               content_type=content_type)
    return request_information


def generate_request_hash(request_information: dict[str, Any]) -> bool:
    simplify_request_str = json.dumps(request_information)
    # get unique hash of the request
    simplify_request_md5 = hashlib.new(
        'md5', simplify_request_str.encode("utf-8")).hexdigest()

    return simplify_request_md5
