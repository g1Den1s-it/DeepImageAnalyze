from pydantic import BaseModel, Field, EmailStr


class UserOutputSchema(BaseModel):
    id: int
    username: str
    email: EmailStr


class UserInputSchema(BaseModel):
    username: str | None = Field(min_length=5, max_length=14, default="username")
    email: EmailStr
    password: str = Field(min_length=8)


class UserSettingSchema(BaseModel):
    username: str | None = Field(min_length=5, max_length=14)
    email: EmailStr | None
    old_password: str | None
    new_password: str | None = Field(min_length=8)
