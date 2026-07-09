from fastapi import FastAPI
from app.logs.logging import setup_logging
from app.core.config import config
from app.api import addresses

setup_logging()

app = FastAPI(title=config.app_name)

app.include_router(addresses.router, prefix='/app/api/addresses.py')