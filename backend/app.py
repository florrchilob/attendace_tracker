import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from routes.attendees_manager import attendees_route
import os
from dotenv import load_dotenv, find_dotenv

logging.basicConfig(level=logging.INFO)
file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('[%(asctime)s] - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.addHandler(file_handler)
logger.propagate = False

# Load environment variables
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

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

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("port", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=True)
