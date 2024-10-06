import os

from dotenv import load_dotenv
from pydantic import BaseConfig

load_dotenv()


class StaticBaseConfig(BaseConfig):
    MEDIA_NAME = os.getenv("MEDIA_NAME", "media")


static_base_config = StaticBaseConfig()
