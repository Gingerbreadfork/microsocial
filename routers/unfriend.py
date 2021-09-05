from fastapi import APIRouter, Depends, Response, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import httpx

from models import *
from shared import *

router = APIRouter()
security = HTTPBasic()

@router.delete("/remove-friend", status_code=200)
def remove_friend(
    deletedfriend: DeletedFriend,
    response: Response,
    credentials: HTTPBasicCredentials = Depends(micro_check)
    ):
    
    check_auth(credentials)
    unfriend = db.get(deletedfriend.key)
    if unfriend == []:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {response}
    
    elif unfriend['category'] == 'friend' or unfriend['category'] == 'pending_friend':
        httpx.post(f"https://{unfriend['bridge']}/public/friend/remove", json = {'key': host_key.decode("utf-8")})
        unfriend_key = unfriend['key']
        db.delete(unfriend_key)
        response.body = "Unfriended Successfully"
        response.status_code = status.HTTP_200_OK
        return {response}
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {response}
    
@router.get("/remove-friend/all", status_code=200)
def remove_all_friends(
    response: Response,
    pending: Optional[bool] = True,
    credentials: HTTPBasicCredentials = Depends(micro_check)
    ):
    
    check_auth(credentials)
    try:
        friends = db.fetch({'category': 'friend'})
        pending = db.fetch({"category": "pending_friend"})
        
        for friend in friends.items:
            httpx.post(f"https://{friend['bridge']}/public/friend/remove", json = {'key': host_key.decode("utf-8")})
            db.delete(friend['key'])
            
        if pending:
            for almost_friend in pending.items:
                httpx.post(f"https://{almost_friend['bridge']}/public/friend/remove", json = {'key': host_key.decode("utf-8")})
                db.delete(almost_friend['key'])
        
        response.body = "All Friends Sucessfully Deleted"
        return {response}
    except:
        response.status_code = status.HTTP_400_BAD_REQUEST
        response.body = "Failed to Delete Friends"
        return {response}