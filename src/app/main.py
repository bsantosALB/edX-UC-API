#from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
import json, os

#Log Configuration
from loguru import logger
from app.config import log_config

logger.remove()
logger.add("./app/logs/file_admin_agent.log", format="{time:YYYY-MM-DD at HH:mm:ss} | {level}: {message} | {function} in line {line} on {file}", rotation="5 MB")

#Database Setup
from app.db import mongo_setup

from app.contract import manage

with open('app/openapi/openapi.json') as json_file:
    tags_metadata = json.load(json_file)


app = FastAPI(
    docs_url="/",
    openapi_tags=tags_metadata,
    openapi_url="/openapi.json",
    title="edX IDSA Provider Use Case API",
    description="""This is an API able to store IDSA-compliant contract information, to ensure proper supply of data to a Sovity consumer"""
)

origins = os.environ["WHITELIST"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

######## Routes to Endpoints in Different Files ########
app.include_router(manage.router)