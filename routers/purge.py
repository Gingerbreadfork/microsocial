from fastapi import APIRouter
from fastapi import Response, status
import time

from shared import *

router = APIRouter()

@router.get("/purge/posts", status_code=200)
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

@router.get("/purge/cache", status_code=200)
def purch_feed_cache(response: Response):
    db.delete("cached_feed")