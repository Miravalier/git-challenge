import aiohttp


base_url = ""
global_params = {}


async def get(endpoint: str, params: dict = None):
    request_params = global_params.copy()
    if params is not None:
        request_params.update(params)
    async with aiohttp.ClientSession() as session:
        async with session.get(base_url + endpoint, params=request_params) as response:
            return await response.json()


async def post(endpoint: str, body: dict = None, params: dict = None):
    request_params = global_params.copy()
    if params is not None:
        request_params.update(params)
    async with aiohttp.ClientSession() as session:
        if body is not None:
            async with session.post(base_url + endpoint, json=body, params=request_params) as response:
                return await response.json()
        else:
            async with session.post(base_url + endpoint, params=request_params) as response:
                return await response.json()


async def put(endpoint: str, body: dict = None, params: dict = None):
    request_params = global_params.copy()
    if params is not None:
        request_params.update(params)
    async with aiohttp.ClientSession() as session:
        if body is not None:
            async with session.put(base_url + endpoint, json=body, params=request_params) as response:
                return await response.json()
        else:
            async with session.put(base_url + endpoint, params=request_params) as response:
                return await response.json()


async def delete(endpoint: str, body: dict = None, params: dict = None):
    request_params = global_params.copy()
    if params is not None:
        request_params.update(params)
    async with aiohttp.ClientSession() as session:
        if body is not None:
            async with session.delete(base_url + endpoint, json=body, params=request_params) as response:
                return await response.json()
        else:
            async with session.delete(base_url + endpoint, params=request_params) as response:
                return await response.json()


async def patch(endpoint: str, body: dict = None, params: dict = None):
    request_params = global_params.copy()
    if params is not None:
        request_params.update(params)
    async with aiohttp.ClientSession() as session:
        if body is not None:
            async with session.patch(base_url + endpoint, json=body, params=request_params) as response:
                return await response.json()
        else:
            async with session.patch(base_url + endpoint, params=request_params) as response:
                return await response.json()
