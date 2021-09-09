from fastapi import APIRouter, Response, status, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import Response
from typing import Optional
import httpx

from shared import *
from models import *

router = APIRouter()
security = HTTPBasic()

async def get_posts(bridge, key):
    posts_endpoint = f"https://{bridge}/public/shared-posts"
    params = {'key': key}
    
    async with httpx.AsyncClient() as client:
        friend_posts = await client.get(posts_endpoint, params=params)
    
    return friend_posts.json()

def check_usernames(friends):
    detected_change = False
    for friend in friends:
        stored_username = friend['name']
        bridge = friend['bridge']
        nameURL = f"https://{bridge}/public/profile"
        latest_username = httpx.get(nameURL)
        new_name = latest_username.json()['username']

        if stored_username != new_name:
            db.update({'name': new_name, 'value': 'notified'}, friend['key'])
            detected_change = True

    return detected_change

@router.get("/friend-posts", status_code=200)
async def read_friend_posts(
    bridge: str,
    response: Response,
    credentials: HTTPBasicCredentials = Depends(micro_check)
    ):
    
    check_auth(credentials)
    friend_obj = db.fetch({'bridge': bridge, 'category': 'friend'})
    friend_key = friend_obj.items[0]['key']
    friend_posts = await get_posts(bridge, friend_key)
    return friend_posts

@router.get("/friend-list")
def friend_list(
    response: Response,
    pending: Optional[bool] = False,
    check_name: Optional[bool] = True,
    credentials: Optional[HTTPBasicCredentials] = Depends(micro_check)
    ):
    
    check_auth(credentials)

    try:
        if pending == True:
            friends = db.fetch([{'category': 'pending_friend'}, {'category': 'friend'}])
            if check_name == True:
                checked_friends = check_usernames(friends.items)
            else:
                checked_friends = friends.items
                
            if checked_friends == False:
                return friends.items
            else:
                updated_friends = db.fetch([{'category': 'pending_friend'}, {'category': 'friend'}])
                return updated_friends.items
        else:
            friends = db.fetch({'category': 'friend'})
            if check_name == True:
                checked_friends = check_usernames(friends.items)
            else:
                checked_friends = friends.items
                
            if checked_friends == False:
                return friends.items
            else:
                updated_friends = db.fetch({'category': 'friend'})
                return updated_friends.items
    except:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {response}