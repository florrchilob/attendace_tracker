from sqlalchemy import create_engine, MetaData
from dotenv import find_dotenv, load_dotenv
from sqlalchemy.orm import Session


dotenv_path = find_dotenv()
load_dotenv(dotenv_path)


user = "root"
password = "password"
# Aa123456123456
# password
host = "localhost"
secret_key="AA123456123456"
port = 3306
database_name = "attendace_tracker"


engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{database_name}")

meta = MetaData()

from sqlalchemy.orm import sessionmaker

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

conn = engine.connect()

