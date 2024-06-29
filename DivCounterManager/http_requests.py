import httpx
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def http_get(url: str):
    logger.info(f'Fetching data from {url}')
    async with httpx.AsyncClient(timeout=10.0) as client:
        result = await client.get(url)
    logger.info(f'Got data, status = {result.status_code}, data = {result.text}')
    return result.text


async def http_post(url: str, uids: list[str]):
    logger.info(f'Posting {uids} to {url}')
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=uids)
    logger.info(f'Posted. {response.status_code=}, {response.text=}')
    return response.text
