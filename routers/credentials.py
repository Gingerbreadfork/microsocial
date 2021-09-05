from fastapi import APIRouter, Depends, Response, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import time

from shared import *
from models import *

router = APIRouter()
security = HTTPBasic()

@router.get("/creds", status_code=200)
def return_credentials(
    credentials: HTTPBasicCredentials = Depends(micro_check)
    ):
    
    check_auth(credentials)
    
    try:
        host_login = db.get("login")['value']
    except TypeError:
        host_login = "admin"
        db.put({'key': 'login', 'value': host_login})
    
    try:
        host_password = db.get("password")['value']
    except TypeError:
        host_password = "password"
        db.put({'key': 'password', 'value': host_password})
    
    return {"login": host_login, "password": host_password}

@router.post("/creds/change", status_code=200)
def change_credentials(
    response: Response,
    newCreds: UpdatedCredentials,
    credentials: HTTPBasicCredentials = Depends(micro_check)
    ):
    
    check_auth(credentials)
    
    try:
        db.put({"key": "login", "value": newCreds.login})
        db.put({"key": "password", "value": newCreds.password})
        response.body = "Credentials updated"
        return {response}

    except:
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    