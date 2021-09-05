from fastapi import APIRouter, Depends
from fastapi import Response, status, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import httpx
import uuid
import time

from models import *
from shared import *

router = APIRouter()
security = HTTPBasic()

@router.get('/messages', status_code=200)
def direct_messages(
    key: str,
    credentials: HTTPBasicCredentials = Depends(micro_check)
    ):
    
    check_auth(credentials)
    try:
        friend = db.get(key)
        if friend['category'] != "friend":
            raise Exception
    except:
        raise HTTPException(
            status_code = 404,
            detail = "Friend Not Found"
            )

    return friend['messages']

@router.post("/messages/respond", status_code=200)
def respond_message(
    message: RespondMessage,
    response: Response,
    credentials: HTTPBasicCredentials = Depends(micro_check)
    ):
    
    check_auth(credentials)
    friend_key = message.key
    friend = db.get(friend_key)
    
    resp = httpx.post(
    f"https://{friend['bridge']}/public/messages/receive",
    json = {'content': message.content, 'key': host_key.decode("utf-8")}
    )
    
    if resp.status_code == 200:
        try:
            messages = friend['messages']
        except:
            messages = []

        messages.append(
            {
                "timestamp": time.time(),
                "message": message.content,
                "uuid": uuid.uuid4().hex,
                "response": True
                }
            )
        
        friend['messages'] = messages

        try:
            db.put(friend)
            response.status_code = status.HTTP_200_OK
            response.body = "Successfully Received Message"
            return {response}
        except:
            response.status_code = status.HTTP_400_BAD_REQUEST
            response.body = "Failed to Receive Message"
            return {response}
    else:
        raise HTTPException(
            status_code = resp.status_code,
            detail = "Failed to Respond to Message"
            )
