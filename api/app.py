from aiohttp import web

from db import init_db, close_db
from routes import setup_routes


async def create_app(config):
    app = web.Application()
    app['config'] = config

    setup_routes(app)
    app.on_startup.append(init_db)
    app.on_cleanup.append(close_db)

    return app
