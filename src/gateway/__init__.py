class GatewayException(Exception):
    pass


class ItemNotFoundException(GatewayException):
    pass


class TimeoutException(GatewayException):
    pass
