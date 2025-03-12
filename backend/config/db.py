from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData
from dotenv import find_dotenv, load_dotenv
import os

load_dotenv() 

DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "attendance_tracker")
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)


engine = create_async_engine(f"mysql+aiomysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

meta = MetaData()

from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


