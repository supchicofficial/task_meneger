from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.filters import Command
from dotenv import load_dotenv
from aiogram.fsm.state import State,StatesGroup
from aiogram.fsm.context import FSMContext 
from service import *
from connection import *
import os
import asyncio

load_dotenv()

token = os.getenv("BOT_TOKEN")

bot = Bot(token=token)
dp = Dispatcher()


from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.filters import Command
from dotenv import load_dotenv
from aiogram.fsm.state import State,StatesGroup
from aiogram.fsm.context import FSMContext 

import os
import asyncio


load_dotenv()

token_bot = os.getenv("BOT_TOKEN")

bot = Bot(token=token_bot)
dp = Dispatcher()

main_kb = ReplyKeyboardMarkup(
   keyboard=[
       [KeyboardButton(text="Add Task")]
       ], resize_keyboard=True,
    
)

class AddTask(StatesGroup):
    get_title = State()
    get_caption = State()
    get_dueration = State()
    get_create = State()
    
class DeleteTask(StatesGroup):
    get_id = State()
    
class UpdateTask(StatesGroup):
    get_id = State()
    get_title = State()
    get_caption = State()
    
@dp.message(F.text == "Add Task")    
@dp.message(Command("add"))
async def add_task(message: Message, state : FSMContext):
    await message.answer("Введите имя таска: ")
    await state.set_state(AddTask.get_title)
    
    
@dp.message(AddTask.get_title)
async def add_task(message: Message, state : FSMContext):
    await state.update_data(title = message.text)
    await message.answer("Введите описания таска: ")
    await state.set_state(AddTask.get_caption)


@dp.message(AddTask.get_caption)
async def add_task(message: Message, state : FSMContext):
    await state.update_data(caption = message.text)
    await message.answer("Ведите дату: ")
    await state.set_state(AddTask.get_dueration)
    


@dp.message(AddTask.get_dueration)
async def add_task(message: Message, state : FSMContext):
    await state.update_data(due_date = message.text)
    data = await state.get_data()
    await create_task(
        data.get("title"),
        data.get("caption"),
        data.get("due_date"),
        message.from_user.id
    )
    await message.answer(f"""
    ✅Задача создана 
    Title: {data.get("title")}
    Caption: {data.get("caption")}
    Dueration date: {data.get("due_date")}
    """)
    await state.clear()


@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("👋Привет мой друг давай создадим задачу?", reply_markup=main_kb)


@dp.message(Command("get_my_tasks"))
async def show_my_tasks(message: Message):
    tasks = await get_task_by_id(message.from_user.id)
    text = ""
    for data in tasks:
        text+= f"""
Id: {data['task_id']}  
Title: {data.get("title")}
Caption: {data.get("caption")}
Dueration date: {data.get("due_date")}
                             """
    await message.answer(text)


@dp.message(Command("update_task"))
async def edit_task_handler(message: Message, command: FSMContext):
    data = command.args.split("/",3)
    if len(data) != 4:
        await message.answer(
            "Нужно указать ID, название, описание и дату."
        )
        return
    task_id, title, caption, due_date = data
    if not task_id.isdigit():
        await message.answer("ID задачи должен быть числом.")
        return    
    pop = await update_task(
        int(task_id),
        title.strip(),
        caption.strip(),
        due_date.strip(),
        message.from_user.id
    )
    if pop:
        await message.answer("✅Сделано")
    else:
        await message.answer(
            "⚠️Ты не создал таск"
        )


@dp.message(Command("delete_task"))
async def delete_task_handler(message: Message, command: FSMContext):
    task_id = command.args.strip()
    if not task_id.isdigit():
        await message.answer("ID задачи должен быть числом.")
        return
    pop = await delete_task(int(task_id), message.from_user.id)
    if pop:
        await message.answer("✅Сделано")
    else:
        await message.answer(
            "⚠️Таск не существует или ты не создал его"
        )



async def main():
    await create_table()
    print("Bot started")
    await dp.start_polling(bot)
    
if __name__ == "__main__":
    asyncio.run(main())