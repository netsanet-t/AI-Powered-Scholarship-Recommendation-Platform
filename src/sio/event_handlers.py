import socketio
from ..auth.services import varify_token

sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins="*"  # mirror CORS policy
)

@sio.event
async def connect(sid, environ, auth):
    """
    Handle a new client connection. Perform simple token-based auth.
    The `auth` argument contains the handshake auth data from the client.
    Raise ConnectionRefusedError to reject the connection if authentication fails.
    """
    try:
        token = auth.get('token')
        token_data = varify_token(token)
        print(f"Client connected: {sid}")
    except ConnectionRefusedError as e:
        await sio.disconnect(sid=sid)
    except Exception as e:
        await sio.disconnect(sid=sid)
    # except 

@sio.event
async def disconnect(sid):
    """Handle client disconnect."""
    print(f"Client disconnected: {sid}")

@sio.event
async def test(sid, data):
    await sio.emit('test', data)

