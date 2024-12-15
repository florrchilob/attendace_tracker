import logging
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from routes.attendees_manager import attendees_route
from models.tables import create
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse


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
    allow_origins=["http://localhost:5174", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(attendees_route)

@app.on_event("startup")
def probando():
    create()

@app.get("/")
def home(request: Request):
    logger.info(f"An application was received in the home page. Endpoint: {request.url.path}")
    return {"data": "Home"}

#ver el 404
# @app.exception_handler(HTTPException)
# def not_fount(request: Request, exc: HTTPException):
#     if exc.status_code == 404:
#         return RedirectResponse(url='/docs')
#         return templates.TemplateResponse(RedirectResponse(url= '/docs'), {"request": request}, status_code=404)