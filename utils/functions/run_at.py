from asyncio import iscoroutine, sleep
from datetime import datetime


# Allows us to schedule coroutine calls w/o breaking asyncio as it doesn't like long sleeps.
async def run_at(runtime: datetime, coro: callable, *args, **kwargs):
    one_day_in_seconds = 86400

    while runtime > datetime.now():
        remaining_seconds = (runtime - datetime.now()).total_seconds()
        seconds_to_sleep = min(remaining_seconds, one_day_in_seconds)
        await sleep(seconds_to_sleep)

    func = coro(*args, **kwargs)

    if iscoroutine(func):
        return await func

    return func
