from fastapi import FastAPI, HTTPException
from app.core.logging import setup_logging
from app.core.config import config


setup_logging()

app = FastAPI(title=config.app_name)
