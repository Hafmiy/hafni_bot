class BotLogicException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class UserInputException(BotLogicException):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)