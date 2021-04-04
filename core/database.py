from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv
from os import environ

load_dotenv()

DB = environ.get("db")
DB_NAME = environ.get("dbname")
DB_USER = environ.get("dbuser")
DB_PSWD = environ.get("dbpwd")
DB_HOST = environ.get("dbhost")
DB_PORT = environ.get("dbport")

SQLALCHEMY_DATABASE_URL = f"{DB}://{DB_USER}:{DB_PSWD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()