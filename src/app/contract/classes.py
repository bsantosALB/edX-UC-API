from typing import Annotated
from pydantic import BaseModel, HttpUrl, Field, AfterValidator
from enum import Enum

from datetime import datetime
import uuid
#HttpUrlString = Annotated[HttpUrl, AfterValidator(lambda v: str(v))]


class ContractDeadline(BaseModel):
    start_date: str
    end_date: str
    
class Contract(BaseModel):
    id: str
    #stakeholderServices: List[SHServices]
    #stakeholderRoles: list[SHRoles] = Field(..., min_items=1)
    #stakeholderRoles: SHRoles
    #handler_url: HttpUrlString
    name: str
    duration: ContractDeadline


def is_valid_uuid(value: str):
    try:
        uuid.UUID(value)
        return True
    except (ValueError, TypeError):
        return False

def is_valid_iso8601_utc(value: str):
    try:
        datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%fZ")
        return True
    except ValueError:
        return False

def parse_iso8601(ts: str):
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))

def is_start_after_end(start_iso: str, end_iso: str):
    start_date = parse_iso8601(start_iso)
    end_date = parse_iso8601(end_iso)
    return start_date > end_date