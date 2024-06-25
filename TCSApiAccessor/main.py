from fastapi import FastAPI
from pydantic import BaseModel
from config import load_config
from datetime import datetime
from schema import Instrument, Instruments


from tcs_api import TCSFetcher

config = load_config()

app = FastAPI()

fetcher = TCSFetcher(config.tcs.token, config.tcs.settings)


@app.get("/get_instruments")
async def provide_instruments():
    return await fetcher.download_instruments()
