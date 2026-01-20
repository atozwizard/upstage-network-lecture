class EmailNotAllowedNameExistsError(Exception):
    def __init__(self, message="Email not allowed or Name already exists"):
        self.message = message
        super().__init__(self.message)

class UserNotFoundError(Exception):
    def __init__(self, message="User not found"):
        self.message = message
        super().__init__(self.message)
