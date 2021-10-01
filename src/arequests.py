import aiohttp


global_params = {}


async def get(endpoint: str, params: dict = None):
    request_params = global_params.copy()
    if params is not None:
        request_params.update(params)
    async with aiohttp.ClientSession() as session:
        async with session.get(GITEA_URL + endpoint, params=request_params) as response:
            return await response.json()


async def post(endpoint: str, data: dict = None, params: dict = None):
    request_params = global_params.copy()
    if params is not None:
        request_params.update(params)
    async with aiohttp.ClientSession() as session:
        if data is not None:
            async with session.post(GITEA_URL + endpoint, json=data, params=request_params) as response:
                return await response.json()
        else:
            async with session.post(GITEA_URL + endpoint, params=request_params) as response:
                return await response.json()


async def put(endpoint: str, data: dict = None, params: dict = None):
    request_params = global_params.copy()
    if params is not None:
        request_params.update(params)
    async with aiohttp.ClientSession() as session:
        if data is not None:
            async with session.put(GITEA_URL + endpoint, json=data, params=request_params) as response:
                return await response.json()
        else:
            async with session.put(GITEA_URL + endpoint, params=request_params) as response:
                return await response.json()


async def delete(endpoint: str, data: dict = None, params: dict = None):
    request_params = global_params.copy()
    if params is not None:
        request_params.update(params)
    async with aiohttp.ClientSession() as session:
        if data is not None:
            async with session.delete(GITEA_URL + endpoint, json=data, params=request_params) as response:
                return await response.json()
        else:
            async with session.delete(GITEA_URL + endpoint, params=request_params) as response:
                return await response.json()


async def patch(endpoint: str, data: dict = None, params: dict = None):
    request_params = global_params.copy()
    if params is not None:
        request_params.update(params)
    async with aiohttp.ClientSession() as session:
        if data is not None:
            async with session.patch(GITEA_URL + endpoint, json=data, params=request_params) as response:
                return await response.json()
        else:
            async with session.patch(GITEA_URL + endpoint, params=request_params) as response:
                return await response.json()
