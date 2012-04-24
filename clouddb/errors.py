class ResponseError(Exception):
    """
    Raised when the remote service returns an error.
    """
    def __init__(self, status, reason):
        self.status = status
        self.reason = reason
        Exception.__init__(self)

    def __str__(self):
        return '%d: %s' % (self.status, self.reason)

    def __repr__(self):
        return '%d: %s' % (self.status, self.reason)


class InvalidRegion(Exception):
    """
    Raised when the region specified is invalid
    """
    pass


class AuthenticationFailed(Exception):
    """
    Raised on a failure to authenticate.
    """
    pass


class InvalidDBInstance(Exception):
    def __init__(self, reason):
        self.reason = reason
        Exception.__init__(self)

    def __str__(self):
        return '%s' % (self.reason)

    def __repr__(self):
        return '%s' % (self.reason)
