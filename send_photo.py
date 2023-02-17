import datetime
import random
import urllib.request

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from bot import bot, TOKEN
from data import list_of_floor, list_of_room
from to_yadisk import load_to_disk


class SendPhoto(StatesGroup):
    waiting_for_floor = State()
    waiting_for_room = State()
    waiting_for_photo = State()


async def send_photo_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for name in list_of_floor:
        keyboard.add(name)
    await message.answer("Выберите этаж:", reply_markup=keyboard)
    await SendPhoto.waiting_for_floor.set()


# Обратите внимание: есть второй аргумент
# Получает номер этажа
async def floor_chosen(message: types.Message, state: FSMContext):
    if message.text.lower() not in list_of_floor:
        await message.answer("Пожалуйста, выберите этаж, используя клавиатуру ниже.")
        return
    await state.update_data(chosen_floor=message.text.lower())

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for size in list_of_room:
        keyboard.add(size)
    # Для последовательных шагов можно не указывать название состояния, обходясь next()
    await SendPhoto.next()
    await message.answer("Теперь выберите помещение:", reply_markup=keyboard)


# Принимает номер и наименование помещения
async def room_chosen(message: types.Message, state: FSMContext):
    if message.text.lower() not in list_of_room:
        await message.answer("Пожалуйста, выберите помещение, используя клавиатуру ниже.")
        return
    await state.update_data(chosen_room=message.text.lower())
    user_data = await state.get_data()
    await SendPhoto.next()
    await message.answer(f"Вы ввели помещение: {user_data['chosen_room']} - {user_data['chosen_floor']}.\n"
                         f"Теперь пришлите мне фотографию", reply_markup=types.ReplyKeyboardRemove())


# Принимает фото
async def get_photo(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    name = user_data['chosen_room']
    floor = user_data['chosen_floor']
    try:
        chat_id = message.chat.id
        make_topic_time = datetime.datetime.now() + datetime.timedelta(hours=3)  # Перевод в Московское время
        make_topic_time = make_topic_time.strftime('%Y_%m_%d-%H_%M')

        document_id = message.photo[-1].file_id
        file_info = await bot.get_file(document_id)

        fi = file_info.file_path

        src_new = f'data/userFiles/{name}__{make_topic_time}__{chat_id}__{random.randrange(100)}.jpeg'
        src_new = src_new.replace(' ', '_')
        print('src_new= ', src_new)
        urllib.request.urlretrieve(f'https://api.telegram.org/file/bot{TOKEN}/{fi}',
                                   src_new)

        with open('data/mainFiles/table_patterns.txt', 'a', encoding='utf-8') as f:
            name_topic = name + '_' + make_topic_time + '_' + '(cod_' + str(random.randrange(10000)) + ')'
            name_topic = name_topic.replace(';', '_')
            name_topic = name_topic.replace(':', '_')
            print(name_topic, message.from_user.id, src_new, True, sep=';', file=f)

        load_to_disk(src_new, floor, name)
        await message.reply("Файл  успешно сохранён")

    except Exception as e:
        print(e)


def register_handlers_send_photo(dp: Dispatcher):
    dp.register_message_handler(send_photo_start, commands="send", state="*")
    dp.register_message_handler(floor_chosen, state=SendPhoto.waiting_for_floor)
    dp.register_message_handler(room_chosen, state=SendPhoto.waiting_for_room)
    dp.register_message_handler(get_photo,
                                content_types='photo',
                                state=SendPhoto.waiting_for_photo)


