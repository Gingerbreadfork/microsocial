from fastapi import APIRouter

from shared import *

router = APIRouter()

@router.get("/my-key", status_code=200)
def show_my_key():
    return {'key': host_key}