from fastapi import APIRouter, status, Depends, Header

from src.auth import service
from src.auth.dependencies import create_user, get_user, get_new_access
from src.auth.schemas import UserOutputSchema, UserInputSchema, TokenSchema

auth = APIRouter(prefix="/auth")


@auth.post('/register/',
           status_code=status.HTTP_201_CREATED,
           response_model=UserOutputSchema)
async def register(user: UserInputSchema = Depends(create_user)):
    return user


@auth.post('/login/',
           status_code=status.HTTP_200_OK,
           response_model=TokenSchema)
async def login(user: UserInputSchema = Depends(get_user)):
    token = await service.create_user_jwt_token(user)
    return token


@auth.get('/refresh/',
          status_code=status.HTTP_200_OK)
async def refresh(token: str = Depends(get_new_access)):
    return {"access": token}
