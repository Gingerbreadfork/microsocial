from fastapi import APIRouter
from fastapi import FastAPI, Response, status
import time
import uuid
import httpx

from models import *
from shared import *
from encryption import *

router = APIRouter()

@router.get("/public/shared-posts", status_code=200)
def shared_posts(
    response: Response,
    key: str,
    limit: Optional[int] = None,
    offset: Optional[int] = None
    ):
    
    my_posts = db.fetch({'category': 'post'})

    for post in my_posts.items:
        del post['category']
        if key.encode('utf8') == host_key:
            post['value'] = decrypt_str_with_key(host_key, post['value'])
    
    sorted_posts = sort_and_trim(my_posts.items, limit, offset)
    return sorted_posts

@router.get("/public/profile", status_code=200)
def get_host_bio():
    host_username = db.get('my_name')
    try:
        host_bio = db.get('my_bio')
        return {'username': host_username['value'], 'bio': host_bio['value']}
    except TypeError:
        host_bio = "Nothing to see here..."
        return {'username': host_username['value'], 'bio': host_bio}
    
@router.post("/public/request", status_code=200)
def request_friend(addfriend: AddFriend, response: Response):
    # You can only lodge a friend request here, approval can only be done via /accept
        try:
            checkFriendExists = db.get(addfriend.public_key)
            checkType = checkFriendExists['category']
            
            if checkType == "friend":
                response.body = "Already a Friend"
                return {response}
            
            elif checkType == "pending_friend":
                response.body = "Already Pending"
                return {response}
            
            else:
                response.body = "Something is Wrong"
                response.status_code = status.HTTP_400_BAD_REQUEST
        
        except:
            pending_friend_json = {
                'key': addfriend.public_key,
                'name': addfriend.name,
                'category': 'pending_friend',
                'bridge': addfriend.bridge
                }
            
            pending_friend = db.put(pending_friend_json)
        
            if pending_friend == pending_friend_json:
                response.status_code = status.HTTP_201_CREATED
                return pending_friend_json

@router.post("/public/notify", status_code=201)
def receive_notification(notification: ReceivedNotif, response: Response):
    friend_data = db.get(notification.key)

    bridge = friend_data['bridge']
    category = friend_data['category']
    key = friend_data['key']

    if category == 'friend' and bridge == notification.bridge and key == notification.key:
        update_check = db.update({'value': 'notified'}, key)
        
        if not update_check:
            response.body = "Notification Created"
            again = db.get(notification.key)
            db.put({'value': time.time()}, "notif_trigger")
            return again

    elif key == host_key:
        response.body = "You Cannot Notify Yourself"
        return {response}
        
    elif key != notification.key:
        response.body = "Unknown or Incorrect Key"
        return {response}

    else:
        response.body = "Unable to Trigger Notification"
        response.status_code = status.HTTP_400_BAD_REQUEST
        
@router.post("/public/react", status_code=200)
def post_reaction(reaction: ReactedPost):
    post_obj = db.get(reaction.postkey)
    
    try:
        reactions = post_obj['reactions']
    except TypeError:
        reactions = []
    
    if {"emoji": reaction.emoji, "reacting": reaction.bridge} not in reactions:
        reactions.append({"emoji": reaction.emoji, "reacting": reaction.bridge})
    else:
        reactions.remove({"emoji": reaction.emoji, "reacting": reaction.bridge})
    
    db.update({'reactions': reactions}, reaction.postkey)
    return reactions

@router.post("/public/messages/receive", status_code=200)
def receive_message(message: ReceivedMessage, response: Response):
    friend_key = message.key
    friend = db.get(friend_key)
    
    try:
        messages = friend['messages']
    except:
        messages = []
    
    messages.append(
        {
            "timestamp": time.time(),
            "message": message.content,
            "uuid": uuid.uuid4().hex,
            "response": False
            }
        )

    try:
        db.update({"messages": messages}, friend_key)
        response.status_code = status.HTTP_200_OK
        response.body = "Successfully Received Message"
        return {response}
    except:
        response.status_code = status.HTTP_400_BAD_REQUEST
        response.body = "Failed to Receive Message"
        return {response}
    
@router.get("/public/messages/clear", status_code=201)
def receive_message(response: Response, key: str, reciprocal: Optional[bool] = False):
    friend = db.get(key)
    
    friend['messages'] = []
  
    if not reciprocal:
        decoded_key = host_key.decode("utf-8")
        httpx.get(
            f"https://{friend['bridge']}/public/messages/clear?key={decoded_key}&reciprocal=True")

    try:
        db.put(friend)
        response.status_code = status.HTTP_200_OK
        response.body = "Successfully Cleared Messages"
        return {response}
    except:
        response.status_code = status.HTTP_400_BAD_REQUEST
        response.body = "Failed to Clear Messages"
        return {response}