from fastapi import APIRouter, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import Response
from typing import Optional
import httpx
import time

from shared import *

router = APIRouter()
security = HTTPBasic()

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
        
@router.get("/feed")
async def friend_feed(
    response: Response,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
    cached: Optional[bool] = False,
    cache: Optional[bool] = False,
    credentials: HTTPBasicCredentials = Depends(micro_check)
    ):
    
    check_auth(credentials)
    
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

@router.get("/notifications", status_code=200)
async def check_notifications(
    clear: Optional[bool] = False,
    credentials: HTTPBasicCredentials = Depends(micro_check)
    ):
    
    check_auth(credentials)
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

@router.get("/last-updated", status_code=200)
def return_last_update_timestamp(credentials: HTTPBasicCredentials = Depends(micro_check)):
    check_auth(credentials)
    try:
        last_updated = db.get("last_updated")['value']
        return {'last_updated': last_updated}
    except:
        updated = db.put(time.time(), 'last_updated')
        return {'last_updated': updated['value']}
