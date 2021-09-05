from fastapi import APIRouter, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from selectolax.parser import HTMLParser
import httpx

from shared import *

router = APIRouter()
security = HTTPBasic()

@router.get("/metatags", status_code=200)
async def get_metatags(
    link: str,
    credentials: HTTPBasicCredentials = Depends(micro_check)
    ):
    
    check_auth(credentials)
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