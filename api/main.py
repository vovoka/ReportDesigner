from aiohttp import web

from app import create_app
from settings import load_config


if __name__ == '__main__':
    config = load_config('config/dev.toml')['database']
    app = create_app(config)
    import aioreloader
    aioreloader.start()
    web.run_app(app)
