from fastapi import FastAPI, Response, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from fastapi.staticfiles import StaticFiles
from selectolax.parser import HTMLParser
import uuid
import time
import httpx

from models import *
from config import *
from encryption import *
from shared import *

from routers import public

app = FastAPI()
app.include_router(public.router)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

async def get_posts_from_friend(friend):
    name = friend['name']
    key = friend['key'].encode('utf8')
    bridge = friend['bridge']
    posts_endpoint = f"https://{bridge}/public/shared-posts"
    params = {"key": key}
    
    async with httpx.AsyncClient() as client:
        friend_posts = await client.get(posts_endpoint, params=params)

    lists_of_posts = friend_posts.json()

    for post in lists_of_posts:
        post['name'] = name
        post['value'] = decrypt_str_with_key(key, post['value'])

    return lists_of_posts

async def get_my_posts():
    my_posts = db.fetch({'category': 'post'})
    latest_username = get_my_name()
    for post in my_posts.items:
        post['name'] = latest_username
        post['value'] = decrypt_str_with_key(host_key, post['value'])
        del post['category']
    
    return my_posts.items

async def replace_posts(friend):
    try:
        cached_feed = db.get("cached_feed")['value']
    except:
        friend_feed()

    for post in cached_feed:
        try:
            if post['bridge'] == friend['bridge']:
                cached_feed.remove(post)
                any_posts = True
        except:
            pass

    if any_posts:
        friend_posts = await get_posts_from_friend(friend)
        cached_feed.append(friend_posts)
        sort_and_trim(cached_feed)
        timestamp = time.time()
        db.put({'value': cached_feed, 'key': "cached_feed"})
        db.put({'value': timestamp, "key":'last_updated'})

@app.post("/add-friend", status_code=200)
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

@app.delete("/remove-friend", status_code=200)
def remove_friend(deletedfriend: DeletedFriend, response: Response):
    unfriend = db.get(deletedfriend.key)
    if unfriend == []:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {response}
    
    elif unfriend['category'] == 'friend' or unfriend['category'] == 'pending_friend':
        unfriend_key = unfriend['key']
        db.delete(unfriend_key)
        response.body = "Unfriended Successfully"
        response.status_code = status.HTTP_200_OK
        return {response}
    
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {response}

@app.post("/create-post", status_code=200)
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

@app.get("/friend-posts", status_code=200)
async def read_friend_posts(bridge: str, response: Response):
    friend_obj = db.fetch({'bridge': bridge, 'category': 'friend'})
    friend_key = friend_obj.items[0]['key']
    friend_posts = await get_posts(bridge, friend_key)
    return friend_posts

@app.get("/friend-list")
def friend_list(response: Response, pending: Optional[bool] = False):
    try:
        if pending == True:
            friends = db.fetch([{'category': 'pending_friend'}, {'category': 'friend'}])
            checked_friends = check_usernames(friends.items)
            if checked_friends == False:
                return friends.items
            else:
                updated_friends = db.fetch([{'category': 'pending_friend'}, {'category': 'friend'}])
                return updated_friends.items
        else:
            friends = db.fetch({'category': 'friend'})
            checked_friends = check_usernames(friends.items)
            if checked_friends == False:
                return friends.items
            else:
                updated_friends = db.fetch({'category': 'friend'})
                return updated_friends.items
    except Exception as e:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {response}

@app.get("/feed")
async def friend_feed(
    response: Response,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
    cached: Optional[bool] = False,
    cache: Optional[bool] = False
    ):
    
    if cached:
        try:
            cached_feed = db.get("cached_feed")['value']
            if cached_feed != None:
                return cached_feed
        except:
            pass
        
    posts = []
    friends = db.fetch({'category': 'friend'})
    my_posts = await get_my_posts()

    for friend in friends.items:
        friend_posts = await get_posts_from_friend(friend)
        posts.append(friend_posts)  
    
    posts.append(my_posts)
    combined = [item for sublist in posts for item in sublist]
    sorted_posts = sort_and_trim(combined, limit, offset)

    if cache:
        db.put(sorted_posts, 'cached_feed')

    return sorted_posts

@app.get("/my-key", status_code=200)
def show_my_key():
    return {'key': host_key}

@app.post("/accept", status_code=200)
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

@app.get("/notifications", status_code=200)
async def check_notifications(clear: Optional[bool] = False):
    try:
        trigger = db.get("notif_trigger")['value']
    except:
        trigger = db.put({'value': time.time()}, "notif_trigger")['value']
    try:
        last_updated = db.get("last_updated")['value']
    except:
        last_updated = db.put({'value': time.time()}, "last_updated")['value']
    
    if trigger > last_updated:
        friends = db.fetch({'category': 'friend'})
        notified_friends = []
        
        for friend in friends.items:
            try:
                if friend['value'] == 'notified':
                    notified_friends.append(friend)
            except:
                return {'notifications': 'Fetching Notifications Failed'}
            
        for friend in notified_friends:
            await replace_posts(friend)    
        
        if clear == False:
            if len(notified_friends) > 0:
                return {'notifications': notified_friends, 'updated': last_updated}
            else:
                return {'notifications': 'No Notifications', 'updated': last_updated}
        else:
            for friend in notified_friends:    
                db.update({'value': 'inactive'}, friend['key'])
            return {'notifications': 'Notifications Cleared', 'updated': last_updated}
    else:
        return {'notifications': 'No Notifications', 'updated': last_updated}

@app.get("/last-updated", status_code=200)
def return_last_update_timestamp():
    try:
        last_updated = db.get("last_updated")['value']
        return {'last_updated': last_updated}
    except:
        updated = db.put(time.time(), 'last_updated')
        return {'last_updated': updated['value']}

@app.put("/edit", status_code=200)
def edit_post(edit: EditingItem, response: Response):
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

@app.get("/metatags", status_code=200)
async def get_metatags(link: str):
    headers = {'user-agent': 'Microsocial', 'Connection': 'keep-alive',}
    
    with httpx.Client() as client:
        link_html = client.get(link, headers=headers)
    
    tree = HTMLParser(link_html.content)

    attrs = {}

    for tag in tree.tags("meta"):
        if "property" in tag.attributes:
            name = tag.attributes["property"]
            attrs[name] = tag.attributes["content"]

    try:
        title = attrs['og:title']
        
        if title == "Internal Error":
            raise Exception
    except:
        title = link

    try:
        description = attrs['og:description']
        
        if description == "Something went wrong":
            raise Exception
    except:
        description = "None"
    
    try:
        image = attrs['og:image']
    except:
        image = "None"
        
    return {'title': title, 'description': description, 'image': image}

@app.get('/messages', status_code=200)
def direct_messages(key: str):
    try:
        friend = db.get(key)
        if friend['category'] != "friend":
            raise Exception
    except:
        raise HTTPException(status_code = 404, detail = "Friend Not Found")

    return friend['messages']

@app.post("/messages/respond", status_code=200)
def respond_message(message: RespondMessage, response: Response):
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
        raise HTTPException(status_code = resp.status_code, detail = "Failed to Respond to Message")

@app.get("/purge/posts", status_code=200)
def purge_posts(response: Response):
    try:
        posts = db.fetch({"category": "post"})
        keys = []
    
        for post in posts.items:
            keys.append(post['key'])
    
        for key in keys:
            db.delete(key)

        db.put({'value': time.time()}, "notif_trigger")['value']
        response.body = "All Posts Purged"
        
        return response
    except:
        response.body = "Failed to Purge Posts"
        response.status_code = status.HTTP_400_BAD_REQUEST
        return response

@app.get("/purge/cache", status_code=200)
def purch_feed_cache(response: Response):
    db.delete("cached_feed")
    
app.mount('', StaticFiles(directory="client/dist/", html=True), name="static")