from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from routers import public, messaging, purge, unfriend
from routers import meta, posting, editing, friending
from routers import feed, friends, keys, credentials

app = FastAPI()

# Routers
app.include_router(public.router)
app.include_router(messaging.router)
app.include_router(purge.router)
app.include_router(unfriend.router)
app.include_router(meta.router)
app.include_router(posting.router)
app.include_router(editing.router)
app.include_router(friending.router)
app.include_router(feed.router)
app.include_router(friends.router)
app.include_router(keys.router)
app.include_router(credentials.router)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mounted Frontend Client
app.mount('', StaticFiles(directory="client/dist/", html=True), name="static")