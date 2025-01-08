from fastapi import FastAPI
from fastapi_socketio import SocketManager

app = FastAPI()
sio = SocketManager(app=app)

@sio.on('connect', namespace='/test')
async def connect(sid, environ):
    print("Cliente conectado!")
    await sio.emit('response', {'data': 'Conexión exitosa'}, room=sid, namespace='/test')

@sio.on('disconnect', namespace='/test')
def disconnect(sid):
    print('Cliente desconectado')