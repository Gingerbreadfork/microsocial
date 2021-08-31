from fastapi import APIRouter
from fastapi import Response, status
import time

from shared import *
from models import *

router = APIRouter()

@router.post("/add-friend", status_code=200)
def add_friend(newfriend: NewFriend, response: Response):
    friend_json = {
        'key': newfriend.public_key,
        'name': newfriend.name,
        'category': 'friend',
        'bridge': newfriend.bridge,
        'value': 'notified'
        }
    
    added_friend = db.put(friend_json)
    
    if added_friend == friend_json:
        return friend_json
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return response

@router.post("/accept", status_code=200)
def accept_friend(addfriend: AddFriend, response: Response):
        try:
            checkFriendExists = db.get(addfriend.public_key)
            checkType = checkFriendExists['category']
            
            if checkType == "friend":
                response.body = "Already Connected"
            
            if checkType == "pending_friend":
                db.update(
                    {
                    'category': 'friend',
                    'name': addfriend.name,
                    'bridge': addfriend.bridge,
                    'value': 'notified',
                    'messages': []
                    }, addfriend.public_key
                        )
                
                db.put(time.time(), 'last_updated')
                response.body = "Connection Request Accepted"
            
            return {response}

        except:
            pending_friend_json = {
                'key': addfriend.public_key,
                'name': addfriend.name,
                'category': 'pending_friend',
                'bridge': addfriend.bridge,
                'value': 'notified'
                }
            
            pending_friend = db.update(pending_friend_json)
        
            if pending_friend == pending_friend_json:
                response.status_code = status.HTTP_201_CREATED
                return pending_friend_json