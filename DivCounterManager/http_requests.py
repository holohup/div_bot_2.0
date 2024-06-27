import httpx


async def http_get(url: str):
    async with httpx.AsyncClient() as client:
        result = await client.get(url)
    return result.text


async def http_post(url: str, uids: list[str]):
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=uids)
    return response.text
