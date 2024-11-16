from tortoise import Tortoise

async def db_init():
    # Коннектимся к SQLite (подставляем свою бд)
    # Также обязательно указать модуль,
    # который содержит модели.
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': ['models']}
    )
    # Генерируем схемы
    await Tortoise.generate_schemas()