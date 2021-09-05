from fastapi import APIRouter, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from shared import *

router = APIRouter()
security = HTTPBasic()

@router.get("/my-key", status_code=200)
def show_my_key(credentials: HTTPBasicCredentials = Depends(micro_check)):
    check_auth(credentials)
    return {'key': host_key}