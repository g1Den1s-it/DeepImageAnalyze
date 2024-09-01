import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

SQL_DATABASE_URL = ('postgresql+psycopg2://{}:{}@{}:{}/{}'
                    .format(os.getenv("DB_USER"),
                            os.getenv("DB_PASSWORD"),
                            os.getenv("DB_HOST"),
                            os.getenv("DB_PORT"),
                            os.getenv("DB_NAME")))

engine = create_engine(SQL_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
