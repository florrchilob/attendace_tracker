import logging
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from routes.attendees_manager import attendees_route
from models.tables import create
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware



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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173","http://localhost:5174", "http://127.0.0.1:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def cors_middleware(request: Request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "http://localhost:5173"
    response.headers["Access-Control-Allow-Methods"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response


app.include_router(attendees_route)

@app.on_event("startup")
def probando():
    create()

@app.get("/")
def home(request: Request):
    logger.info(f"An application was received in the home page. Endpoint: {request.url.path}")
    return {"data": "Home"}
