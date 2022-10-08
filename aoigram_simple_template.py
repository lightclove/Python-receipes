import logging

from aiogram import Bot, Dispatcher, executor, types
# Then you have to initialize bot and dispatcher instances. Bot token you can get from @BotFather
#API_TOKEN = 'PLACE BOT TOKEN HERE'
API_TOKEN = 'Insert_your_token_here'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Next step: interaction with bots starts with one command. Register your first command handler:
@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")

# If you want to handle all text messages in the chat simply add handler without filters:
@dp.message_handler()
async def echo(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)
    await message.answer(message.text)

# Last step: run long polling.
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
