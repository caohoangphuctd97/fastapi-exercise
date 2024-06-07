class UserNotFound(Exception):
    def __str__(self):
        return "UserNotFound"


class UserExisted(Exception):
    def __str__(self):
        return "UserExisted"


class ServerErrorException(Exception):
    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return self.message
