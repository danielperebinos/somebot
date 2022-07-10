import logging

from aiogram import Bot, Dispatcher, executor, types
from db import JSONDatabase
from markups import skip_menu, start_menu


API_TOKEN = '5598475740:AAE2G2fELuHIEIXNBndQ-qdJMnc7j073P7M'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
database = JSONDatabase()

ADMIN_ID = '1094576056'

# Message Handlers
@dp.message_handler(commands=['start', 'Start'])
async def start(message: types.Message):
    await message.reply("Would you like to add a new project ?", reply_markup=start_menu)

@dp.message_handler()
async def chat(message: types.Message):
    user_id = str(message.from_user.id)
    step = database.get_user_step(user_id)

    if step == 'name_project':
        database.insert_data(user_id, step, str(message.text))
        await bot.send_message(message.from_user.id, 'In a few words, describe the main goals that your project is trying to achieve')

    elif step == 'goals':
        database.insert_data(user_id, step, str(message.text))
        await bot.send_message(message.from_user.id,
                               'If applicable, send any legal documentation that will further be reviewed manually by our team',
                               reply_markup=skip_menu)
    elif step == 'members':
        database.insert_data(user_id, step, str(message.text))
        await bot.send_message(message.from_user.id,
                               'We thank you for all the provided information, we shall get back to you in 2-5 Business days , if accepted, you will receive a personal message from our admins')

        data = database.user_data_complete(str(message.from_user.id))
        data.pop('skip')
        if data:
            await bot.send_message(ADMIN_ID, data)
            for message_id in data['documents']:
                await bot.forward_message(chat_id=ADMIN_ID, from_chat_id=message.from_user.id, message_id=message_id)

        await bot.send_message(message.from_user.id,
                               'We have already sent your request. For creating one more just type /start')


@dp.message_handler(content_types=['photo'])
async def photo_receiver(message: types.Message):
    if database.get_user_step(str(message.from_user.id)) in ('documents'):
        database.insert_data(str(message.from_user.id), key='documents', value=message.message_id)

    await bot.send_message(message.from_user.id, 'For continue press skip', reply_markup=skip_menu)
    # await bot.forward_message(chat_id=message.from_user.id, from_chat_id=message.from_user.id, message_id=message.message_id)


# Callback query handlers
@dp.callback_query_handler(text='yes')
async def start_project(message: types.Message):
    await bot.send_message(message.from_user.id,
                           text= 'We are glad that you have decided to join our team, Please send the following information')
    await bot.send_message(message.from_user.id, text='Name of your project:')

@dp.callback_query_handler(text='no')
async def dont_start(message: types.Message):
    await bot.send_message(message.from_user.id, 'Have a nice day')


@dp.callback_query_handler(text='skip')
async def skip_document(message: types.Message):
    database.insert_data(str(message.from_user.id), 'skip', True)
    await bot.send_message(message.from_user.id, text='Please send a list of all the member involved in creating this project')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)