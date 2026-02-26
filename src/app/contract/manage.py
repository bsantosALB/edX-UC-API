from typing import Annotated
from fastapi import APIRouter, Response, status, Query, Header
from fastapi.responses import JSONResponse, FileResponse
import requests, json, sys, os, time, threading, copy

from pathlib import Path

from loguru import logger
from bson import ObjectId

#from app.authentication import authentication
from app.db import mongo_setup

from datetime import datetime, timezone
from app.contract import classes
# classes
from app.contract.classes import Contract

BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR / "../files" / os.environ["CSV_FILE_NAME"]


router = APIRouter(
    prefix="/contract",
    tags=["contract"]
)


@router.post("/register", status_code=201, responses={201: {"model": Contract}})
async def register_contract(body: Contract): #, shared_secret: Annotated[str, Header()]
    #check if uuid contract already exists
    try:
        subscriber = mongo_setup.contract_collection.find_one({"id": body.dict()["id"]}, {"_id": 0})
        if subscriber is not None:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content="Contract with this UUID already registered")

    except Exception as error:
        logger.error(error)
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content="Unable to verify existing Contract")

    try:
        #UUID Format validation
        if classes.is_valid_uuid(body.dict()["id"]) is False:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content="Invalid UUID Format")
        
        #Dates ISO 8601 validation
        if classes.is_valid_iso8601_utc(body.dict()["duration"]["start_date"]) is False and classes.is_valid_iso8601_utc(body.dict()["duration"]["end_date"]) is False:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content="Invalid Date Format, should be in ISO 8601 format")

        #check if start date is later than end date
        if classes.is_start_after_end(body.dict()["duration"]["start_date"], body.dict()["duration"]["end_date"]) is True:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content="Start Date is later than End Date")

        #check if dates are equal
        if body.dict()["duration"]["start_date"] == body.dict()["duration"]["end_date"]:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content="Start Date cannot be equal to End Date")

        mongo_setup.contract_collection.insert_one(body.dict())
        return body

    except Exception as error:
        logger.error(error)
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content="Unable to store Contract request on Database")
            

@router.get("/{contract_id}", responses={200: {"model": Contract}})
async def read_specific_contract(contract_id: str):
    try:
        subscriber = mongo_setup.contract_collection.find_one({"id": contract_id}, {"_id": 0})
        if subscriber == None:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content="Contract non existent or not found")
        else: 
            return subscriber

    except Exception as error:
        logger.error(error)
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content="Unable to read specific Contract")


@router.get("/", responses={200: {"model": list[Contract]}})
async def query_contracts():
    try:
        result = list(mongo_setup.contract_collection.find({}, {"_id": 0}))
        return result

    except Exception as error:
        logger.error(error)
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content="Unable to fetch Contracts on Database")


@router.delete("/{contract_id}", responses={200: {"model": list[Contract]}})
async def delete_contract(contract_id: str):
    try:
        subscriber = mongo_setup.contract_collection.find_one_and_delete({"id": contract_id}, {"_id": 0})
        if subscriber == None:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content="Contract non existent or not found")
        else: 
            return JSONResponse(status_code=status.HTTP_200_OK, content="Contract successfully deleted")

    except Exception as error:
        logger.error(error)
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content="Unable to delete Contract on Database")


@router.get("/{contract_id}/file")
async def get_contract_file(contract_id: str):
    try:
        subscriber = mongo_setup.contract_collection.find_one({"id": contract_id}, {"_id": 0})
        if subscriber == None:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content="Contract non existent or not found")
        else: 
            #check if CSV download is authorized (between start and end date)
            current_time = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")

            if subscriber["duration"]["start_date"] <= current_time <= subscriber["duration"]["end_date"]:    
                if not CSV_PATH.exists():
                    raise HTTPException(status_code=404, detail="File not found")
                else:
                    return FileResponse(
                        path=CSV_PATH,
                        media_type="text/csv",
                        filename=os.environ["CSV_FILE_NAME"],
                        headers={
                            "Cache-Control": "no-store",
                            "Pragma": "no-cache",
                        }
                    )
    
            else:
                return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content="File access has expired")

    except Exception as error:
        logger.error(error)
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content="Unable to download Contracted CSV Data")