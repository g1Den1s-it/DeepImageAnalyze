from fastapi import APIRouter, status, Depends

from src.auth.dependencies import create_user
from src.auth.schemas import UserOutputSchema, UserInputSchema

auth = APIRouter(prefix="/auth")


@auth.post('/register/',
           status_code=status.HTTP_201_CREATED,
           response_model=UserOutputSchema)
async def register(user: UserInputSchema = Depends(create_user)):
    return user


@auth.post('/log-in/')
async def login():
    pass


@auth.get('/refresh/')
async def refresh():
    pass
