import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from routes.attendees_manager import attendees_route

logging.basicConfig(level=logging.INFO)
file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('[%(asctime)s] - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.addHandler(file_handler)
logger.propagate = False

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.include_router(attendees_route)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
