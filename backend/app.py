import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from routes.attendees_manager import attendees_route


# Configurar logging
logging.basicConfig(level=logging.INFO)
file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('[%(asctime)s] - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.addHandler(file_handler)
logger.propagate = False

# Crear aplicación FastAPI
app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.include_router(attendees_route)

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5173/attendees", "http://localhost:80", "http://localhost:80/attendees"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
