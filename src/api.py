import arequests
import os


# Environment variables
GITEA_TOKEN = os.environ['GITEA_TOKEN']
GITEA_URL = os.environ['GITEA_URL']
if GITEA_URL.endswith('/'):
    GITEA_URL = GITEA_URL[:-1]


# Global configuration
arequests.base_url = GITEA_URL
arequests.global_params["access_token"] = GITEA_TOKEN


# Wrappers
get = arequests.get
put = arequests.put
post = arequests.post
patch = arequests.patch
delete = arequests.delete


async def users() -> dict:
    return {user["login"]: user for user in await get("/admin/users/")}


async def create_user(username: str, password: str) -> dict:
    return await post("/admin/users", body={
        "email": f"{username}@miramontes.dev",
        "login_name": username,
        "must_change_password": False,
        "password": password,
        "username": username,
        "visibility": "private",
    })

async def create_repo(username: str, repo: str, description: str = None) -> dict:
    body = {
        "name": repo,
        "auto_init": False,
        "private": True,
    }
    if description is not None:
        body["description"] = description

    return await post(f"/admin/users/{username}/repos", body=body)

async def add_key(username: str, title: str, key: str) -> dict:
    body = {
        "title": title,
        "key": key,
        "read_only": False,
    }
    return await post(f"/admin/users/{username}/keys", body=body)
