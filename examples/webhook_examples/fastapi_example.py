# -*- coding: utf-8 -*-
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from aiotgram import AioTGram


app = FastAPI()

bot = AioTGram('<bot_token>')

bot.set_webhook('<server_url>')


@app.post('/')
async def handler(request: Request):
    data = await request.json()

    return JSONResponse({'ok': True})
