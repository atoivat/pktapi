from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv
from os import environ

load_dotenv()

DB = environ.get("DB")
DB_NAME = environ.get("DB_NAME")
DB_USER = environ.get("DB_USER")
DB_PSWD = environ.get("DB_PSWD")
DB_HOST = environ.get("DB_HOST")
DB_PORT = environ.get("DB_PORT")

SQLALCHEMY_DATABASE_URL = f"{DB}://{DB_USER}:{DB_PSWD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# print(SQLALCHEMY_DATABASE_URL)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()