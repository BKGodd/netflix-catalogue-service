from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import ResponseValidationError
from elasticsearch import AsyncElasticsearch
from string import punctuation
from unidecode import unidecode as ud
import os
from collections import ChainMap

import schemas
from database import get_elastic_db, init_elastic_db

app = FastAPI(openapi_url="/api/docs/openapi.json",
              docs_url="/api/docs/")

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://nginx:80'], # Where the frontend is hosted
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set Elasticsearch dependency
async def get_db():
    esdb = get_elastic_db()
    try:
        yield esdb
    finally:
        await esdb.close()

esdb = get_elastic_db()

@app.on_event("startup")
async def startup():
    """"""
    #esdb = await get_db().__anext__()
    await init_elastic_db(esdb)

@app.on_event("shutdown")
async def shutdown():
    """"""
    #await esdb.close()

