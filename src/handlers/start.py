from . import *

router = Router()


@router.message(Command('start'))
async def start(message: types.Message, state: FSMContext):
    await message.answer('Hello!')
 