import api
import asyncio
import functools
import os

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from lxml import etree
from lxml.html.builder import *
from starlette.responses import RedirectResponse


INDEX = etree.tostring(HTML(
    HEAD(
        TITLE("Git Challenge"),
        SCRIPT("", src="https://code.jquery.com/jquery-3.6.0.min.js"),
        SCRIPT("", src="/challenge/static/challenge.js"),
        LINK(rel="stylesheet", href="/challenge/static/challenge.css"),
        LINK(rel="preconnect", href="https://fonts.googleapis.com"),
        LINK(rel="preconnect", href="https://fonts.gstatic.com"),
        LINK(href="https://fonts.googleapis.com/css2?family=Lato&display=swap", rel="stylesheet"),
    ),
    BODY(
        DIV(
            DIV(
                SPAN("Username", {"class": "label"}),
                INPUT({"class": "input"}, type="text", id="username"),
                {"class": "field"},
            ),
            DIV(
                BUTTON("Verify", type="button", id="verify"),
                {"class": "field"},
            ),
            {"id": "inputs", "class": "section"}
        ),
        DIV(
            {"id": "challenges", "class": "section"}
        ),
    ),
), pretty_print=True)


async def not_found_handler(request, exc):
    return RedirectResponse(url="/404", status_code=303)


app = FastAPI(root_path="/challenge", exception_handlers={404: not_found_handler})
app.mount("/static", StaticFiles(directory="static"), name="static")


class TestContext:
    def __init__(self):
        self.user = None
        self.repository = None
        self.ref = None

    async def set_user(self, username: str):
        self.user = username

    async def set_repository(self, repository: str):
        self.repository = repository
        response = await api.get(f"/repos/{self.user}/{self.repository}")
        if response.get('message') == 'Not Found':
            raise Exception(
                f"The user {self.user} does not have a repository named {self.repository}"
            )

    async def set_branch(self, branch: str):
        self.ref = branch
        response = await api.get(f"/repos/{self.user}/{self.repository}/branches/{self.ref}")
        if response.get('message') == 'Not Found':
            raise Exception(
                f"The {self.repository} repository does not have a {self.ref} branch"
            )

    async def commits(self, value: int):
        response = await api.get(f"/repos/{self.user}/{self.repository}/commits", params={"sha": self.ref})
        if isinstance(response, dict) and response.get("message") == "Git Repository is empty.":
            raise Exception(
                f"The {self.repository} repository has no commits."
            )
        print("DEBUG Commits", response)
        if len(response) != value:
            raise Exception(
                f"There must be {value} commit(s) in the {self.ref} branch "
                f"of the {self.repository} repo, but I found {len(response)}"
            )

    async def file(self, path: str, content: str = ""):
        response = await api.get(f"/repos/{self.user}/{self.repository}/contents/{path}", params={"ref": self.ref})
        print("DEBUG File", response)
        if response.get("content") != content:
            raise Exception(
                f"The contents of the file '{path}' on the {self.ref} branch "
                f"of the {self.repository} repo are incorrect."
            )

    async def no_file(self, path: str):
        response = await api.get(f"/repos/{self.user}/{self.repository}/contents/{path}", params={"ref": self.ref})
        print("DEBUG No File", response)
        if response.get("content") is not None:
            raise Exception(
                f"The file '{path}' on the {self.ref} branch "
                f"of the {self.repository} repo must not exist."
            )


def challenge_check(func):

    @functools.wraps(func)
    async def checked_func(*args, **kwargs):
        ctx = TestContext()
        try:
            await func(ctx, *args, **kwargs)
            return {"status": "pass"}
        except BaseException as e:
            return {"status": "fail", "reason": str(e)}

    return checked_func


@challenge_check
async def check_alpha(ctx: TestContext, username: str):
    await ctx.set_user(username)
    await ctx.set_repository("Alpha")

    await ctx.set_branch("master")
    await ctx.commits(1)
    await ctx.file("README.md", "# Challenge: Alpha\nGet this directory pushed!\n")
    await ctx.file("file1", "")
    await ctx.file("file2", "")
    await ctx.file("file3", "")


@challenge_check
async def check_beta(ctx: TestContext, username: str):
    await ctx.set_user(username)
    await ctx.set_repository("Beta")

    await ctx.set_branch("revert_branch")
    await ctx.commits(3)
    await ctx.file("file_a", "Lorem\n")
    await ctx.no_file("file_b")

    await ctx.set_branch("erase_branch")
    await ctx.commits(1)
    await ctx.file("file_a", "Lorem\n")
    await ctx.no_file("file_b")


@app.get("/{username}/verify")
async def verify(username: str):
    # Make sure user exists
    users = await api.users()
    if username not in users:
        raise HTTPException(status_code=404, detail="Invalid username")

    # Get results
    results = {
        "Alpha": await check_alpha(username),
        "Beta": await check_beta(username),
    }

    # Return results
    return {"username": username, "results": results}


@app.get("/", response_class=HTMLResponse)
async def index():
    return INDEX
