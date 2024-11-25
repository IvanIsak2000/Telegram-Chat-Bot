# Base `aiogram` bot template

# Setup
- `python3.12`
- `sqlalchemy`
- `psycopg2`
- `logging`
- `poetry`


# How to use?
1. Clone repository

2. Activate `poetry` and install dependencies
```bash
poetry install && poetry shell
```

3. Fill `.env` file by your data
4. [Get bot token from BotFather](https://core.telegram.org/bots/faq#how-do-i-create-a-bot)

5. Change folder
```bash
cd src/
```

5. Add your code!

6. Run bot
```bash
python3 bot.py
```

# How use with database?
1. Fill `.env` file with `postgresql` data of your db server
2. Uncomment the database initialization in the `bot.py` file
3. Uncomment `models` import in `handlers/__init__.py`
4. Uncomment middleware import in `bot.py` and middleware connect
