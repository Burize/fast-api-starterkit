class CustomException(Exception):
    @property
    def message(self):
        return self.args[0] if self.args else ''



class NotFoundException(CustomException):
    pass