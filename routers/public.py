from fastapi import APIRouter
from fastapi import FastAPI, Response, status

from models import *
from shared import *

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