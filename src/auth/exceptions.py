from fastapi import HTTPException


class UserNotCreated(HTTPException):
    def __init__(self):
        self.message = "User already created!"
        super().__init__(status_code=409, detail=self.message)
