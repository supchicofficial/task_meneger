from dotenv import load_dotenv
import asyncpg
import os

load_dotenv()
pasw  = os.getenv("PASSWORD_DB")

async def connection_db():
    try:
        conn = await asyncpg.connect(
            host="localhost",
            port=5432,
            user="postgres",
            database="bot2_db",
            password=pasw
        )
        return conn
    except Exception as Error:
        print(f"Connection Error: {Error}")
        
async def create_table():
    try:
        conn = await connection_db()
        await conn.execute("""
Create table if not exists users(
    user_id serial primary key,
    username varchar(100),
    full_name varchar(100),
    telegram_id varchar(200),
    created_at timestamp default now(),
    is_active boolean default true
);
   
Create table if not exists tasks(
    task_id serial primary key,
    title varchar(100),
    caption text,
    telegram_id varchar(200),
    created_at timestamp default now(),
    status boolean default false,
    is_active boolean default true

)                 
                     """)
        print("Table created")
    except Exception as Error:
        print(f"Create Error: {Error}")
    finally:
        await conn.close()