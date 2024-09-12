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


class UnauthorizedUser(HTTPException):
    def __init__(self):
        self.message = "Unauthorized User!"
        super().__init__(status_code=401, detail=self.message)


class InvalidToken(HTTPException):
    def __init__(self):
        self.message = "Invalid User Token!"
        super().__init__(status_code=401, detail=self.message)


class TypeToken(HTTPException):
    def __init__(self):
        self.message = "Invalid token type!"
        super().__init__(status_code=401, detail=self.message)


class ExpiredToken(HTTPException):
    def __init__(self):
        self.message = "Token has expired!"
        super().__init__(status_code=401, detail=self.message)
