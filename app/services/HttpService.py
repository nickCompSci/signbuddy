import aiohttp

class AsyncHttpClient:
    def __init__(self) -> None:
        self._session = aiohttp.ClientSession()

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args, **kwargs):
        await self.close()

    async def post_image(self, url, data, bearerToken):
        print(bearerToken)
        headers = {
            'content-type': "application/json",
            'authorization': f"Bearer {bearerToken}"
        }
        async with self._session.post(url, json=data, headers=headers ) as r:
            return await r.json()
        
    async def post_auth0_management_api_token(self, url, data):
        headers= {'content-type': "application/x-www-form-urlencoded"}
        async with self._session.post(url, data=data, headers=headers ) as r:
            return await r.json()
        
    async def post_auth0_signbuddymodel_api_token(self, url, data):
        headers= {'content-type': "application/json"}
        async with self._session.post(url, json=data, headers=headers ) as r:
            return await r.json()
        
    async def get_current_user(self, url, data, bearerToken):
        headers = {
            'content-type': "application/json",
            'authorization': f"Bearer {bearerToken}"
        }
        async with self._session.get(url, data=data, headers=headers ) as r:
            return await r.json()

    async def close(self) -> None:
        if not self._session.closed:
            await self._session.close()