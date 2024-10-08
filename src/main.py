import uvicorn
from fastapi import FastAPI

from src.auth.router import auth

app = FastAPI()

app.include_router(auth)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
