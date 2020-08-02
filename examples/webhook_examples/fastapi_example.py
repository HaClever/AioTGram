# -*- coding: utf-8 -*-
import asyncio

import aiotgram

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.routing import Route


bot = aiotgram.AioTGram('<bot_token>')


async def startup_actions():
    await bot.set_webhook('<url>')

    await bot.enable_save_next_step_handlers(delay=2)
    await bot.load_next_step_handlers()


async def handler(request: Request):
    request_body_dict = await request.json()
    update = await aiotgram.types.Update.de_json(request_body_dict)

    return JSONResponse({"status": "success"}, status_code=200)


def get_routes():
    routes = [
        Route('/', handler, methods=["GET", "POST"])
    ]
    return routes


app = FastAPI(routes=get_routes())

asyncio.get_running_loop().create_task(startup_actions())
