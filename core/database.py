from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import Engine

from dotenv import load_dotenv
from os import environ

load_dotenv()

TESTING_DB_URL = environ.get("TESTING_DB_URL")
if TESTING_DB_URL:
    # Testing database (sqlite)
    DATABASE_URL = TESTING_DB_URL
else:
    # Production database (postgres)
    DB = environ.get("DB")
    DB_NAME = environ.get("DB_NAME")
    DB_USER = environ.get("DB_USER")
    DB_PSWD = environ.get("DB_PSWD")
    DB_HOST = environ.get("DB_HOST")
    DB_PORT = environ.get("DB_PORT")

    DATABASE_URL = f"{DB}://{DB_USER}:{DB_PSWD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

print(DATABASE_URL)

if TESTING_DB_URL:
    # Testing database (sqlite)
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

    # Code to trigger foreign key checks on sqlite
    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(connection, *args):
        cursor = connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

else:
    # Production database (postgres)
    engine = create_engine(DATABASE_URL)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()