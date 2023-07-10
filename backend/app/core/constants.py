
# Default POST data content-type
DEFAULT_CONTENT_TYPE = "application/x-www-form-urlencoded"

# Raw text POST data content-type
PLAIN_TEXT_CONTENT_TYPE = "text/plain"

# json text POST data content-type
JSON_TEXT_CONTENT_TYPE = "application/json"

# form text POST data content-type
FORM_DATA_CONTENT_TYPE = "multipart/form-data"


# Just a temporary solution, by right should get the id from database
class Status(object):
    WAITING = 1
    RUNNING = 2
    DONE = 3
    KILLED = 4


class Severity(object):
    LOW = 5
    MEDIUM = 6
    HIGH = 7


class VulnerabilityType(object):
    XSS = 8


class Vulnerability(object):
    REFLECTED_XSS = 1
    STORED_XSS = 2
    DOM_XSS = 3
