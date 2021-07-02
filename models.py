from pydantic import BaseModel

class NewPost(BaseModel):
    access_key: str
    value: str
    
class NewFriend(BaseModel):
    access_key: str
    name: str
    bridge: str
    public_key: str
    
class DeletedFriend(BaseModel):
    access_key: str
    key: str
    
class NewKey(BaseModel):
    access_key: str
    new_key: str

class NewName(BaseModel):
    access_key: str
    new_name: str
    
class AddFriend(BaseModel):
    name: str
    bridge: str
    public_key: str
    
class NewBio(BaseModel):
    bio: str
    
class ReceivedNotif(BaseModel):
    bridge: str
    key: str