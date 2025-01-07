import logging
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi_socketio import SocketManager  # Asegúrate de instalar fastapi-socketio
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
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurar SocketManager
socket_manager = SocketManager(app=app, mount_location="/socket.io")

# Evento de inicio
@app.on_event("startup")
def startup_event():
    logger.info("Aplicación iniciada correctamente.")

# Evento de cierre
@app.on_event("shutdown")
def shutdown_event():
    logger.info("Aplicación cerrada correctamente.")

# Ruta HTTP básica
@app.get("/")
def home():
    logger.info("Acceso a la página de inicio.")
    return {"message": "Bienvenido a la API con WebSockets"}

# Ruta WebSocket de ejemplo
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    logger.info("Cliente conectado al WebSocket.")
    try:
        while True:
            data = await websocket.receive_text()
            logger.info(f"Mensaje recibido: {data}")
            await websocket.send_text(f"Mensaje recibido: {data}")
    except Exception as e:
        logger.error(f"Error en WebSocket: {e}")
    finally:
        await websocket.close()
        logger.info("Cliente desconectado del WebSocket.")
