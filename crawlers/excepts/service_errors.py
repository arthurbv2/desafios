class ServiceError(Exception):

    def __init__(self, message):
        self.message = message


class InexistentSubRedditError(ServiceError):

    def __init__(self, message):
        super().__init__(message)
