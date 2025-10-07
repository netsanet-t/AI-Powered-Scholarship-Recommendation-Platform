from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
# import socketio

# from .sio.event_handlers import sio
from .exceptions import register_app_exceptions
from .api import register_routers
from .logging import config_level, LogLevels
from .database.core import Base, async_engine
from .dependencies.dependencies import lifespan

from .setting import origins

config_level(log_level=LogLevels.INFO)


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def startup():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)



app.mount("/api/v1/static", StaticFiles(directory="public/images"), name="static")

register_routers(app)
register_app_exceptions(app)

# app = socketio.ASGIApp(socketio_server=sio, other_asgi_app=app)