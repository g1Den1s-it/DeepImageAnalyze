import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.auth.router import auth
from src.config import static_base_config
from src.report.router import report_router

app = FastAPI()

app.include_router(auth)
app.mount("/media", StaticFiles(directory=static_base_config.MEDIA_NAME), name=static_base_config.MEDIA_NAME)
app.include_router(report_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
