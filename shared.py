from fastapi import HTTPException, status, Request
from fastapi.security import HTTPBasic
from operator import itemgetter
from deta import Deta
import os
import secrets
import string
import time
import secrets
import random

from encryption import *
from config import *
from wordlists import animals, adjectives

security = HTTPBasic()

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
        username = (random.choice(adjectives)).capitalize()  + " " +  (random.choice(animals)).capitalize()
        db.put({'key': 'my_name', 'value': username})
        
    return username

def check_auth(credentials):
    if credentials is not None:
        try:
            host_login = db.get('login')['value']
        except TypeError:
            host_login = "admin"
            db.put({'key': 'login', 'value': host_login})

        try:
            host_password = db.get('password')['value']
        except TypeError:
            host_password = "password"
            db.put({'key': 'password', 'value': host_password})
            
        correct_login = secrets.compare_digest(credentials.username, host_login)
        correct_password = secrets.compare_digest(credentials.password, host_password)

        if not (correct_login and correct_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Basic"},
            )

async def micro_check(request: Request):
    # Set in config.py
    if localdev:
        return None 
    
    if (os.getenv('DETA_RUNTIME')):
        return await security(request) 
    else:
        return None

# Grab Personal Info to Keep it Handy
host_key = get_my_key()
username = get_my_name()