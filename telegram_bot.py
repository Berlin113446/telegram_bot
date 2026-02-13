from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
import asyncio

TOKEN = "Ваш_токен_бота"
OWNER_ID = # Ваш aйді
GROUP_ID = # Айді групи    

TAGS = ["ваші_теги"]

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Перевірка тегів у повідомленні
def extract_tag(text: str):
    for tag in TAGS:
        if tag in text.lower():
            return tag
    return None

# Обробка будь-яких повідомлень
@dp.message()
async def handle_message(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username or "Немає"
    full_name = message.from_user.full_name
    phone = getattr(message.from_user, "phone_number", "Немає")

    tag = extract_tag(message.text)

    # Відправляємо всю інфо тільки власнику
    await bot.send_message(
        OWNER_ID,
        f"🔔 Нове повідомлення від користувача:\n"
        f"ID: {user_id}\n"
        f"Username: @{username}\n"
        f"Name: {full_name}\n"
        f"Телефон: {phone}\n"
        f"Повідомлення:\n{message.text}"
    )

    # Надсилаємо повідомлення користувачу про відсутній тег
    if tag is None:
        await message.reply(
            "❗ Радимо додати тег адміна. Доступні теги:\n" + "\n".join(TAGS)
        )

    # Відправляємо повідомлення в групу (завжди)
    await bot.send_message(GROUP_ID, message.text)

# Команда бану
@dp.message(Command("ban"))
async def cmd_ban(message: Message):
    if message.from_user.id != OWNER_ID:
        await message.reply("❌ Тільки власник може банити користувачів.")
        return

    try:
        user_id = int(message.get_args())
        await bot.ban_chat_member(GROUP_ID, user_id)
        await message.reply(f"✅ Користувач {user_id} забанений у групі.")
    except Exception as e:
        await message.reply(f"❌ Помилка: {e}")

# Команда статусу
@dp.message(Command("status"))
async def cmd_status(message: Message):
    if message.from_user.id == OWNER_ID:
        await message.answer("Привіт, ваш юзернейм ✅ Все працює.")
    else:
        await message.answer("Тільки власник може бачити статус.")

async def main():
    print("Бот запущений...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
