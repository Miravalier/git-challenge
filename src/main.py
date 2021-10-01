import api
import asyncio
import os

from fastapi import FastAPI, HTTPException
from lxml import etree
from lxml.builder import E
from starlette.responses import RedirectResponse


ASDF_PAGE = etree.tostring(E.html(
    E.head(
        E.title("Git Challenge"),
    ),
    E.body(
        E.h1("Test"),
    ),
))


async def not_found_handler(request, exc):
    return RedirectResponse(url="/404", status_code=303)


app = FastAPI(root_path="/challenge", exception_handlers={404: not_found_handler})


@app.get("/{username}/verify")
async def verify(username: str):
    users = await api.users()
    if username not in users:
        raise HTTPException(status_code=404, detail="Invalid username")
    return {"username": username, "success": True}
