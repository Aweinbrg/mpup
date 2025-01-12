import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import asyncio

# Токен бота Telegram
API_TOKEN = '7640871011:AAEbt9QMexrfIgV7Yfv2EMPWX2Rk7RzBihE'

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Простая база данных пользователей (словарь)
user_data = {}

# Кнопка фарма
farm_button = InlineKeyboardMarkup(row_width=1)
farm_button.add(InlineKeyboardButton("🚀 Фармить MPUP", callback_data='farm'))

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_data:
        user_data[user_id] = {'balance': 0}
    await message.answer("🐾 Добро пожаловать в MOONPUP FARM! Нажимай кнопку, чтобы фармить MPUP!", reply_markup=farm_button)

# Обработчик кнопки фарма
@dp.callback_query_handler(lambda c: c.data == 'farm')
async def process_farm(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user_data[user_id]['balance'] += 1  # +1 MPUP за клик
    await bot.answer_callback_query(callback_query.id, text=f"💰 Ты заработал 1 MPUP! Твой баланс: {user_data[user_id]['balance']} MPUP")

# Обработчик команды /balance
@dp.message_handler(commands=['balance'])
async def check_balance(message: types.Message):
    user_id = message.from_user.id
    balance = user_data.get(user_id, {'balance': 0})['balance']
    await message.answer(f"🪙 Твой текущий баланс: {balance} MPUP")

# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
