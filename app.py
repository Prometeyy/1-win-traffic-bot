from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from uvicorn import run

from const import app_config

from infra.dbase import db


def get_application(
        app_config: dict
) -> dict:
    """
    app_config = {
        "app_name": str,
        "router": APIRouter,
        "docs_url": str,
        "host": str,
        "port": int,
        "base_prefix": str,
        "title": str,
        "description": str
    }
    """
    print(f'⚙️ Building app {app_config["app_name"]}...')
    app = FastAPI(
        docs_url=app_config["docs_url"],
        title=app_config["title"],
        description=app_config["description"],
        root_path='api'
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            'http://localhost:5173',
            'http://localhost:5173',
            'http://localhost',
            'https://timetracker-664ce.web.app/',
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(
        router=app_config["router"],
        prefix=app_config["base_prefix"]
    )

    @app.on_event('startup')
    async def startup():
        print('⚙️ Initialize database...')
        db.build_sql_init_file()
        await db.init_pool()
        # await db.init_tables()
        print('✅ Init success!')

    @app.on_event('shutdown')
    async def shutdown():
        await db.close_pool()

    print('✅ Build success!')
    return {
        'app': app,
        'host': app_config['host'],
        'port': app_config['port']
    }


def run_application(app: dict):
    run(
        app=app['app'],
        host=app['host'],
        port=app['port'],
    )


run_application(
    app=get_application(
        app_config
    )
)
