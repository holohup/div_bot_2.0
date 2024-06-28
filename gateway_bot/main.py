from datetime import datetime
import json
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
import httpx
from config import load_config
import logging
from tabulate import tabulate

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

config = load_config()

bot = Bot(config.bot.token)
dp = Dispatcher()
client = httpx.AsyncClient()


@dp.message(Command(commands="list"))
async def list_tickers(message: Message):
    response = await client.get(config.service.list)
    msg = "List of available tickers with at least 1 future:\n" + response.text
    await message.answer(msg)


@dp.message()
async def dividend_info(message: Message):
    ticker = message.text.upper()
    response = await client.get(config.service.ticker(ticker))
    result = json.loads(response.text)
    if (
        "result" in result.keys()
        and "Instrument with futures not found" in result["result"]
    ):
        await message.reply(result["result"])
    else:
        await message.reply(format_message(ticker, result))


def format_message(ticker, result) -> str:
    result = result["dividends"]
    table_data = [
        [
            f["ticker"],
            datetime.fromisoformat(f["expires"]).strftime("%d-%m-%y"),
            f["dividend"],
        ]
        for f in result
    ]
    headers = ["Ticker", "Expires", "Dividend"]
    table = tabulate(table_data, headers=headers, tablefmt="plain")

    lines = table.split("\n")
    words = [line.split() for line in lines]
    max_lengths = [max(len(word) for word in column) for column in zip(*words)]

    padded_lines = []
    for line in words:
        padded_line = " | ".join(
            word.ljust(max_lengths[i]) for i, word in enumerate(line)
        )
        padded_lines.append(padded_line)

    result = f"{ticker}\n```\n" + "\n".join(padded_lines) + "\n```"
    return result


if __name__ == "__main__":
    dp.run_polling(bot)