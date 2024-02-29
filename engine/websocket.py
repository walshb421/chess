#!/usr/bin/env python

import asyncio
from websockets.server import serve

async def server(callback):
    async with serve(callback, "0.0.0.0", 8765):
        await asyncio.Future()  # run forever
