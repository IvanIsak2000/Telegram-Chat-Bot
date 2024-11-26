from . import *
import ollama

router = Router()


@router.message(Command('start'))
async def start(message: types.Message, state: FSMContext):
    await message.answer('Write your request:')


@router.message(F.text)
async def ask_llm(message: types.Message):
    response = ollama.chat(model='llama3.2:1b', messages=[
        {
            'role': 'user',
            'content': message.text,
        },
    ])
    response_text = response['message']['content']
    await message.answer(text=f'🤖: {response_text}')
