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
