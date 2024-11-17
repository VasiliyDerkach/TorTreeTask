
TORTOISE_ORM = {
        "connections": {
            "default": "sqlite://db.sqlite3"
            },
        "apps": {
            "models": {

                "models": ["TaskTreeApp.models", "aerich.models"],
                "default_connection": "default",
            },
        }
    }
