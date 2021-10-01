import arequests
import asyncio
import os
from fastapi import FastAPI


GITEA_TOKEN = os.environ['GITEA_TOKEN']
GITEA_URL = os.environ['GITEA_URL']
if not GITEA_URL.endswith('/'):
    GITEA_URL += '/'


arequests.global_params["access_token"] = GITEA_TOKEN


app = FastAPI(root_path="/verify")


@app.post("/{username}")
async def verify(username):
    return {"username": username, "success": True}
