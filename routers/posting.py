from fastapi import APIRouter
from fastapi import Response, status
import uuid
import time

from shared import *
from models import *

router = APIRouter()

@router.post("/create-post", status_code=200)
def create_post(newpost: NewPost, response: Response):
    if len(newpost.value) > 2500:
        response.body = "Post is too long"
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {response}
    
    post_id = uuid.uuid4().hex
    timestamp_now = time.time()
    encrypted_post = encrypt_str_with_key(host_key, newpost.value)
    
    post_json = {
        "key": post_id,
        'value': encrypted_post.decode('utf8'),
        'category': 'post',
        'time': timestamp_now,
        'edited': False,
        'reactions': [],
        'bridge': newpost.bridge
        }
    
    create_post = db.put(post_json)

    if create_post == post_json:
        response.body = "Post Created"
        db.put(time.time(), 'last_updated')
        return {response}
    else:
        response.body = "Error Creating Post"
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {response}