from . import *

from utils.ai import AI

router = Router()


@router.message(Command('start'))
async def start(message: types.Message):
    await message.answer('''
Привет! Я Гуринович GPT, обученный на информации о Эдуарде Гуриновиче. 
Спроси меня любой вопрос и я отвечу:''')


@router.message(F.text)
async def ask_llm(message: types.Message, bot: aiogram.Bot):

    if (await bot.get_me()).username in message.text:
        await message.reply(
            text=await AI().ask(message=message.text)
        )
    else:
        if message.chat.type == 'private':
            await message.reply(
                text=await AI().ask(message=message.text)
            )
