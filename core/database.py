from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from core.settings import settings

DB_USER = settings.db_user
DB_PASS = settings.db_password
DB_HOST = settings.db_host
DB_NAME = settings.db_name
DB_PORT = settings.db_port

URL_DATABASE = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'


engine = create_engine(URL_DATABASE) # tool to connect to the database

Session = sessionmaker(bind=engine) # used to interact with database
session = Session()

Base = declarative_base()

Base.metadata.create_all(engine)