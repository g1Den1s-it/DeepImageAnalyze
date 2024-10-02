import uvicorn
from fastapi import FastAPI

from src.auth.router import auth
from src.report.router import report_router

app = FastAPI()

app.include_router(auth)
app.include_router(report_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
