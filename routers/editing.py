from fastapi import APIRouter, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import Response, status
import time

from shared import *
from models import *

router = APIRouter()
security = HTTPBasic()

@router.put("/edit", status_code=200)
def edit_post(
    edit: EditingItem,
    response: Response,
    credentials: HTTPBasicCredentials = Depends(micro_check)
    ):
    
    check_auth(credentials)
    if edit.item == "post":
        try:
            if edit.content and edit.delete == False:
                post_data = db.get(edit.key)
                if post_data['category'] == 'post':
                    new_post = encrypt_str_with_key(host_key, edit.content)
                    db.update({'value': new_post.decode('utf8'), 'edited': True}, edit.key)
                    db.put(time.time(), 'last_updated')
                    response.body = "Post Updated"
                    response.status_code = 200
                    return {response}

            elif edit.delete:
                post_data = db.get(edit.key)
                if post_data['category'] == 'post':
                    db.delete(edit.key)
                    db.put(time.time(), 'last_updated')
                    response.body = "Post Deleted"
                    return {response}

        except:
            response.body = "Post Not Found or Not a Post"
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {response}
        
    elif edit.item == "bio":
        if edit.delete:
            db.put({'key': 'my_bio', 'value': ""})
            response.body = "Bio Deleted"
            return {response}
        else:
            if len(edit.content) > 5000:
                response.body = "Bio is too long"
                response.status_code = status.HTTP_400_BAD_REQUEST
                return {response}
            else:
                db.put({'key': 'my_bio', 'value': edit.content})
                response.body = "Bio Updated"
                return {response}

    elif edit.item == "username":
        if edit.delete:
            response.body = "Can't Delete Username Only Modify It"
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {response}
        else:
            if len(edit.content) <= 20:
                db.put({'key': 'my_name', 'value': edit.content})
                db.put(time.time(), 'last_updated')
                response.body = "Username Updated"
                return {response}
            else:
                response.body = "Username too Long"
                response.status_code = status.HTTP_400_BAD_REQUEST
                return {response}
