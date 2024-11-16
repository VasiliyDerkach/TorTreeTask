from tortoise import Tortoise
from .models import *

async def db_init():
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': ['TaskTreeApp.models']}
    )
    await Tortoise.generate_schemas()

import asyncio
asyncio.run(db_init())