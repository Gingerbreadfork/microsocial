from operator import itemgetter
from deta import Deta
import os
import secrets
import string

from encryption import *
from config import *

def sort_and_trim(posts, limit=None, offset=None):
    try:
        sorted_posts = sorted(posts, key=itemgetter('time'), reverse=True)
        
        if offset is not None and limit is not None:
            trimmed_posts = sorted_posts[offset:offset+limit]
            
        elif limit is not None and offset is None:
            trimmed_posts = sorted_posts[:limit]
            
        elif offset is not None and limit is None:
            trimmed_posts = sorted_posts[offset:]
        else:
            return sorted_posts
            
        return trimmed_posts
    
    except Exception as e:
        return None

# For Local Dev Throw Deta Project Key in .detakey
if os.path.isfile(".detakey"):
    with open(".detakey") as projectkey_file:
        projectkey = projectkey_file.read()
        deta = Deta(projectkey)
else:
    deta = Deta()
    
db = deta.Base(dbname)

def get_my_key():
    try:
        host_access_key_obj = db.get('host_key')
        host_key = host_access_key_obj['value'].encode()
    except TypeError:
        host_key = Fernet.generate_key()
        db.put({'key': 'host_key', 'value': host_key.decode('utf-8')})

    return host_key

def get_my_name():
    try:
        name_obj = db.get('my_name')
        username = name_obj['value']
    except:
        username = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(6))
        db.put({'key': 'my_name', 'value': username})
        
    return username

# Grab Personal Info to Keep it Handy
host_key = get_my_key()
username = get_my_name()