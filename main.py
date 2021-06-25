from fastapi import FastAPI, Response, status
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from fastapi.staticfiles import StaticFiles
from deta import Deta
import logging as log
import uuid
import time
import httpx
from operator import itemgetter
from pydantic import BaseModel

log.basicConfig(level=log.INFO)

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

deta = Deta()
db = deta.Base("microsocial")
database_items = db.fetch()

class NewPost(BaseModel):
    my_name: str
    access_key: str
    post: str
    
class NewFriend(BaseModel):
    access_key: str
    name: str
    bridge: str
    public_key: str
    
class DeletedFriend(BaseModel):
    access_key: str
    name: str

def get_my_key():
    fetchedkey = next(db.fetch({'type': 'my_key'}))

    if fetchedkey == []:
        log.warning("No Private Key Exists! Creating key")
        db.put({'key': uuid.uuid4().hex, 'type': 'my_key'})

    try:
        private_key = fetchedkey[0]['key']
    except:
        fetchedkey = next(db.fetch({'type': 'my_key'}))
        private_key = fetchedkey[0]['key']
    
    return private_key

async def get_posts(name):
    friend = next(db.fetch({'name': name,'type': 'friend'}))
    key = friend[0]['key']
    bridge = friend[0]['bridge']
    posts_endpoint = f"{bridge}shared-posts"
    params = {'access_key': key}
    
    async with httpx.AsyncClient() as client:
        friend_posts = await client.get(posts_endpoint, params=params)
    
    return friend_posts.json()

# Grab Personal Key at Launch
private_key = get_my_key()

@app.post("/add-friend", status_code=200)
def root(newfriend: NewFriend, response: Response):
    if newfriend.access_key == private_key:
        friend_json = {'key': newfriend.public_key, 'name': newfriend.name, 'type': 'friend', 'bridge': newfriend.bridge}
        added_friend = db.put(friend_json)
        
        if added_friend == friend_json:
            return friend_json
        else:
            response.status_code = status.HTTP_404_NOT_FOUND
            return response

    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {response}

@app.delete("/remove-friend", status_code=200)
def remove_friend(deletedfriend: DeletedFriend, response: Response):
    unfriend = next(db.fetch({'name': deletedfriend.name}))
    if deletedfriend.access_key == private_key:
        if unfriend == []:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {response}
        
        else:
            unfriend_key = unfriend[0]['key']
            db.delete(unfriend_key)
            response.status_code = status.HTTP_200_OK
            return {response}

    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {response}

@app.get("/shared-posts", status_code=200)
def read_post(access_key: str, response: Response):
    if access_key == private_key:
        my_posts = db.fetch({'type': 'post'})
        response = [item for sublist in my_posts for item in sublist]
        return response
    
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {response}
    
@app.post("/create-post", status_code=200)
def create_post(newpost: NewPost, response: Response):
    if NewPost.access_key == private_key:
        post_id = uuid.uuid4().hex
        timestamp_now = time.time()
        post_json = {"key": post_id, "post": newpost.post, 'type': 'post', 'time': timestamp_now, 'name': newpost.my_name}
        create_post = db.put(post_json)

        if create_post == post_json:
            response.status_code = status.HTTP_200_OK
            return {response}
        else:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {response}

    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {response}
        
@app.get("/friend-posts", status_code=200)
async def read_friend_posts(name: str, access_key: str, response: Response):
    if access_key == private_key:
        friend_posts = await get_posts(name)
        return {'posts': friend_posts}

    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {response}

@app.get("/friend-list")
def friend_list(access_key: str, response: Response):
    if access_key == private_key:
        friends = next(db.fetch({'type': 'friend'}))
        return friends
    
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {response}
    
@app.get("/friend-feed")
async def friend_feed(access_key: str, response: Response):
    if access_key == private_key:
        posts = []

        friends = next(db.fetch({'type': 'friend'}))
        
        for friend in friends:
            key = friend['key']
            bridge = friend['bridge']
            posts_endpoint = f"{bridge}shared-posts"
            params = {'access_key': key}
        
            async with httpx.AsyncClient() as client:
                friend_posts = await client.get(posts_endpoint, params=params)

            posts.append(friend_posts.json())

        my_posts = next(db.fetch({'type': 'post'}))
        posts.append(my_posts)


        combined = [item for sublist in posts for item in sublist]

        try:        
            sorted_feed = sorted(combined, key=itemgetter('time'), reverse=True)
            return sorted_feed
        except:
            return None
    
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {response}

@app.post("/change-key")
def change_key(access_key: str, new_key: str, response: Response):
    # This very much needs to be private/authed to only the owner
    global private_key
    if access_key == private_key:
        db.put({'key': new_key, 'type': 'my_key'})
        private_key = new_key
        response.status_code = status.HTTP_200_OK
        return {response}

    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {response}
    
@app.get("/my-key")
def show_my_key():
    # This very much needs to be private/authed to only the owner
    return {'key': private_key}

app.mount('', StaticFiles(directory="svelte/dist/", html=True), name="static")
