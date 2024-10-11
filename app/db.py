import os
import asyncpg
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

async def connect_to_db():
    return await asyncpg.connect(DATABASE_URL)

async def log_request(user_id, command, response):
    conn = await connect_to_db()
    await conn.execute('''
        INSERT INTO logs(user_id, command, response, created_at) VALUES($1, $2, $3, NOW())
    ''', user_id, command, response)
    await conn.close()
