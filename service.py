from connection import * 

async def create_user(username, full_name, telegram_id):
    try:
        conn = await connection_db()
        await conn.execute("""
        insert into users(username, full_name, telegram_id) Values
        ($1, $2, $3) 
                     """, username, full_name,str(telegram_id))
    except Exception as Error:
        print(f"Create user Error: {Error}")
    finally:
        await conn.close()


async def get_user_by_id(telegram_id):
    try:
        conn = await connection_db()
        user = await conn.fetchrow("""
        select * from users where telegram_id = $1
                     """, str(telegram_id))
        return user
    except Exception as Error:
        print(f"Get user by id Error: {Error}")
    finally:
        await conn.close()
        

async def get_users():
    try:
        conn = await connection_db()
        users = await conn.fetch("""
        select * from users
                     """)
        return users
    except Exception as Error:
        print(f"Get user Error: {Error}")
    finally:
        await conn.close()
                
         
async def create_task(title, caption, due_date, telegram_id):
    try:
        conn = await connection_db()
        await conn.execute("""
        insert into tasks(title, caption, due_date, telegram_id) Values
        ($1, $2, $3, $4) 
                     """, title, caption, due_date, str(telegram_id))
        return True 
    except Exception as Error:
        print(f"Create task Error: {Error}")
        return False
    finally:
        await conn.close()


async def get_task_by_id(telegram_id):
    try:
        conn = await connection_db()
        user = await conn.fetch("""
        select * from tasks where telegram_id = $1
                     """, str(telegram_id))
        return user
    except Exception as Error:
        print(f"Get task by id Error: {Error}")
    finally:
        await conn.close()



async def update_task(task_id, title, caption, due_date, telegram_id):
    conn = None
    try:
        conn = await connection_db()
        result = await conn.execute("""
        UPDATE tasks
        Set title = $1,
        caption = $2,
        due_date = $3
        Where task_id = $4
        And telegram_id = $5
        And is_active = TRUE
    """, title, caption, due_date, int(task_id), str(telegram_id))
        return result == "UPDATE 1"
    except Exception as Error:
        print(f"Update task Error: {Error}")
        return False
    finally:
        if conn is not None:
            await conn.close()


async def get_my_tasks(telegram_id):
    try:
        conn = await connection_db()
        tasks = await conn.fetch("""
        select * from tasks where telegram_id = $1
                     """, str(telegram_id))
        return tasks
    except Exception as Error:
        print(f"Get my tasks Error: {Error}")
    finally:
        await conn.close()


async def delete_task(task_id, telegram_id):
    conn = None
    try:
        conn = await connection_db()
        result = await conn.execute(
    """
        Delete from tasks
        Where task_id = $1
        And telegram_id = $2
        And is_active = TRUE
    """, int(task_id), str(telegram_id))
        return result == "DELETE 1"
    except Exception as Error:
        print(f"Delete task Error: {Error}")
        return False
    finally:
        if conn is not None:
            await conn.close()