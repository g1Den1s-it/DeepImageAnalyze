from fastapi import HTTPException


class UserNotCreated(HTTPException):
    def __init__(self):
        self.message = "User already created!"
        super().__init__(status_code=409, detail=self.message)


class UserNotFound(HTTPException):
    def __init__(self):
        self.message = f"User not found!"
        super().__init__(status_code=404, detail=self.message)


class WrongPassword(HTTPException):
    def __init__(self):
        self.message = f"Wrong password!"
        super().__init__(status_code=400, detail=self.message)
