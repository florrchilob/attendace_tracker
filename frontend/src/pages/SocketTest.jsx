import { io } from 'socket.io-client';
import { useEffect } from 'react';

function TestSocket() {
  useEffect(() => {
    const socket = io("http://localhost:8000", {
      transports: ['websocket'],
      path: "/socket.io",
      namespace: '/test'
    });

    socket.on('connect', () => {
      console.log('Conectado al namespace /test');
    });

    socket.on('response', (data) => {
      console.log('Mensaje del servidor:', data);
    });

    socket.on('disconnect', () => {
      console.log('Desconectado del namespace /test');
    });

    socket.on('connect_error', (error) => {
      console.error('Error de conexión:', error);
    });

    return () => {
      socket.disconnect();
    };
  }, []);

  return <div>Probando Conexión WebSocket</div>;
}

export default TestSocket;