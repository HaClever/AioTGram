# -*- coding: utf-8 -*-
import asyncio


class Timer:
    # NOTE: need more tests.
    def __init__(self, timeout, callback):
        self._timeout = timeout
        self._callback = callback
        self._task = asyncio.create_task(self._job())

    async def _job(self):
        await asyncio.sleep(self._timeout)
        await self._callback()

    async def is_alive():
        resturn self._task.done()

    async def cancel(self):
        self._task.cancel()
