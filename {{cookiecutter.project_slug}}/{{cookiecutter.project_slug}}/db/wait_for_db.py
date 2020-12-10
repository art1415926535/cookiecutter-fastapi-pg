import asyncio

from databases import Database


async def async_wait_for_db(pg_dsn: str, tries: int = 1, delay: float = 1.0):
    exc = Exception()

    for _ in range(tries):
        try:
            db = Database(pg_dsn)
            await db.connect()
            await db.disconnect()
            return
        except ConnectionRefusedError as e:
            exc = e
            await asyncio.sleep(delay)
            continue

    raise exc


def sync_wait_for_db(pg_dsn: str, tries: int = 1, delay: float = 1.0):
    asyncio.run(async_wait_for_db(pg_dsn, tries, delay))
