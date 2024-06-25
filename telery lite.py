import wikipediaapi
from pyrogram import Client, filters
import random
import asyncio
import requests
import os
from pyrogram.errors import FloodWait
from datetime import datetime, timedelta
import tgcrypto
import subprocess
import sys
import time
import io

# Читает файл "userbot.info", чтобы узнать данные пользователя. Необходимо для всех команд.
with open("userbot.info", "r") as file:
    lines = file.readlines()
    api_id = int(lines[0].strip())
    api_hash = lines[1].strip()
    userid_telegram = int(lines[2].strip())
    prefix_userbot = lines[3].strip()
    allowed_user_id = userid_telegram

# Стандартные переменные. Не меняйте, если не хотите ошибок.
afk_mode = False
afk_reason = ""
afk_start_time = 0
last_command_time = {}
app = Client("telery_userbot", api_id=api_id, api_hash=api_hash)

# Делает запрос на сайт википедии с помощью модуля "wikipedia-api".
wiki_wiki = wikipediaapi.Wikipedia(
    language='ru',
    extract_format=wikipediaapi.ExtractFormat.WIKI,
    user_agent='TeleryUserBot/1.0'
)


# Команда "help"
@app.on_message(filters.command("help", prefixes=prefix_userbot))
async def help_command(_, message):
    prefix = prefix_userbot
    await message.reply_text(
        "**Команды(всего команд: 16):**\n"
        "Команды для пользователя юб:\n"
        f"ℹ`{prefix}info` - инфо о юзерботе\n"
        f"`{prefix}animtext` - анимирует текст.\n"
        f"⌛`{prefix}ping` - Пишет пинг юб.\n"
        f"✉`{prefix}spam` - Начинает флудить сообщением, которое вы выбрали. Пример: `{prefix}spam 3 Telery - круто!`\n"
        f"💤`{prefix}off` - Отключает юзербота.\n"
        f"`.prefix` - Изменяет префикс юзербота. Стандартный префикс: `.`\n"
        f"😴`{prefix}afk` - включает AFK-режим.\n"
        f"🥱`{prefix}afkoff` - отключает AFK-режим.\n"
        "**Команды для всех:**\n"
        f"🔎`{prefix}search` - Ищет информацию в интернете.\n"
        f"⌛`{prefix}time` - Показывает время пользователя юб.\n"
        f"`{prefix}oorr` - Орёл или решка.\n"
        f"🐱`{prefix}randkomaru` / `rk` - кидает рандомную гифку с Комару\n"
        f"❓`{prefix}who` - выбирает рандомного чела, и пишет кто он.\n"
        f"🎰`{prefix}caz` - делает ставку на что-угодно. пример: `{prefix}caz 2 доллара`\n"
        f"🧮`{prefix}math` - решает математические задачи\n"
        f"🔄`{prefix}swap` - Изменить раскладку текста.\n"
    )


# Команда "info"
@app.on_message(filters.me & filters.command("info", prefixes=prefix_userbot))
async def info_command(_, message):
    start_time = time.time()
    await message.delete()
    end_time = time.time()
    ping_time = round((end_time - start_time) * 1000, 1)
    user = message.from_user
    username = f"[{user.first_name} {user.last_name}](https://t.me/{user.username})"
    await app.send_photo(
        chat_id=message.chat.id,
        photo="https://user-images.githubusercontent.com/149149385/278584536-1dab252e-9fd4-4a0c-a80e-5e16c1220eaa.jpg",
        caption=f"**✨Telery**\n"
                f"__🔧Version: 1.8.1 Lite__\n"
                f"Source: @telery_userbot2\n"
                f"**Lite-version💚**\n"
                f"**Ping: {ping_time}ms**\n"
                f"User: {username}"
    )


# Команда "caz"
@app.on_message(filters.command(["caz"], prefixes=prefix_userbot))
async def caz_command(_, message):
    user_id = message.from_user.id
    current_time = time.time()
    if user_id in last_command_time and current_time - last_command_time[user_id] < 1:
        await message.reply_text("**✋Не так часто!**")
        return
    await asyncio.sleep(4)
    bet_split = message.text.split(f"{prefix_userbot}caz ", 1)
    if len(bet_split) < 2:
        await message.reply_text("Некорректная ставка!")
        return
    bet = bet_split[1]
    try:
        bet_amount, bet_text = bet.split(maxsplit=1)
        bet_amount = int(bet_amount)
        if bet_amount <= 0:
            await message.reply_text("**Ставка должна быть положительным числом!**")
            return
    except (ValueError, IndexError):
        await message.reply_text("**Некорректная ставка!**")
        return
    result = random.choice([0, 1])
    if result == 0:
        loss_amount = bet_amount
        await message.reply_text(f"**😢Проигрыш! Вы проиграли {loss_amount} {bet_text}**")
    else:
        win_amount = bet_amount * 2
        await message.reply_text(f"**🥳Выигрыш! Вы выиграли {win_amount} {bet_text}**")
    last_command_time[user_id] = current_time


# Команда "animtext"
@app.on_message(filters.command("animtext", prefixes=prefix_userbot) & filters.me)
async def animtext_command(_, message):
    input_text = message.text.split("animtext ", maxsplit=1)[1]
    temp_text = input_text
    edited_text = ""
    typing_symbol = "█"
    while edited_text != input_text:
        try:
            await message.edit(edited_text + typing_symbol)
            time.sleep(0.1)
            edited_text = edited_text + temp_text[0]
            temp_text = temp_text[1:]
            await message.edit(edited_text)
            time.sleep(0.1)
        except FloodWait:
            print("Превышен лимит сообщений в секунду. Подождите...")


# Команда "who"
@app.on_message(filters.command("who", prefixes=prefix_userbot))
def who_command(client, message):
    prefix = prefix_userbot
    user_id = message.from_user.id
    current_time = time.time()
    if user_id in last_command_time and current_time - last_command_time[user_id] < 1:
        response = "**✋Не так часто!**"
        time.sleep(1)
        app.delete_messages(chat_id, message_id)
    else:
        args = message.text.split()[1:]
        if args:
            members_count = client.get_chat_members_count(message.chat.id)
            members = client.get_chat_members(message.chat.id, limit=members_count)
            random_user = random.choice(list(members)).user
            response = f"@{random_user.username} {' '.join(args)}"
        else:
            response = f"❌Неверно написано. Пример:\n`{prefix}who милый`"
        last_command_time[user_id] = current_time
    app.send_message(message.chat.id, response)


# Команда "rk/randkomaru"
@app.on_message(filters.command(["randkomaru", "rk"], prefixes=prefix_userbot))
async def send_random_komaru_gif(_, message):
    url = 'https://raw.githubusercontent.com/Blaing-7542/BD_Telery/main/komarugifbd'
    response = requests.get(url)
    if response.status_code == 200:
        gifs = response.text.split('\n')
        random_gif = random.choice(gifs)
        await message.reply_animation(random_gif)
    else:
        await message.reply('**😢Не удалось получить гифку. Попробуйте позже.**')
        last_command_time[user_id] = current_time


# Команда "oorr"
@app.on_message(filters.command(["oorr"], prefixes=prefix_userbot))
def oorr_command(_, message):
    random_number = random.randint(0, 1)
    if random_number == 0:
        coin_emoji = "🌑"
        result = "🦅Выпал орёл!"
    else:
        coin_emoji = "🌑"
        result = "🪙Выпала решка!"
    message.reply_text(coin_emoji)
    time.sleep(2)
    message.reply_text(result)


# Команда "ping"
@app.on_message(filters.me & filters.command(["ping"], prefixes=prefix_userbot))
def ping(_, message):
    start_time = time.time()
    msg = message.edit("🌕")
    end_time = time.time()
    ping_time = round((end_time - start_time) * 1000)
    msg.edit("**🕛Ваш пинг: {} мс**".format(ping_time))


# Команда "time"
@app.on_message(filters.command(["time"], prefixes=prefix_userbot))
def send_time(_, message):
    user_id = message.from_user.id
    current_time = datetime.now().strftime("%H:%M:%S")
    if user_id in last_command_time and time.time() - last_command_time[user_id] < 1:
        message.reply_text("Не так часто!")
    else:
        message.reply_text(f"**⌛Время пользователя: {current_time}**")
        last_command_time[user_id] = time.time()


# Команда "math"
@app.on_message(filters.command(["math"], prefixes=prefix_userbot))
def calculate_math(_, message):
    command = message.text.split(" ", 1)[1]
    forbidden_chars = (
        "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v",
        "w",
        "x", "y", "z", "а", "б", "в", "г", "д", "е", "ё", "ж", "з", "и", "й", "к", "л", "м", "н", "о", "п", "р", "с",
        "т",
        "у", "ф", "х", "ц", "ч", "ш", "щ", "ъ", "ы", "ь", "э", "ю", "я", "!", "@", "#", "$", "%", "^", "&", "(", ")",
        "_",
        "=", "{", "}", "[", "]", ";", "'", "<", ">", ",", ".", "?", "<", ">", "«", "**")
    if any(char in command for char in forbidden_chars):
        message.reply("⛔Такие слова писать запрещено!")
    else:
        try:
            result = eval(command)
            message.reply(f"{command} = {result}")
        except Exception as e:
            message.reply(f"⛔Произошла ошибка: {str(e)}")


# Команда "search"
@app.on_message(filters.command(["search"], prefixes=prefix_userbot))
def search_command(_, message):
    query = message.text.split(' ', 1)[1]
    page_py = wiki_wiki.page(query)
    if page_py.exists():
        response = "**🧠Нашёл ответ:**\n\n" + page_py.text[:1024]
        message.edit_text(response)
    else:
        message.edit_text("❌Статья не найдена на Википедии.")


# Команда "spam"
@app.on_message(filters.me & filters.command(["spam"], prefixes=prefix_userbot))
def spam_message(_, message):
    prefix = prefix_userbot
    _, count, *words = message.text.split()
    count = int(count)
    text = ' '.join(words)
    message.delete()
    for _ in range(count):
        app.send_message(message.chat.id, text)


# Команда "off"
@app.on_message(filters.me & filters.command(["off"], prefixes=prefix_userbot))
def turn_off(_, message):
    message.edit("**💤Отключаю юзербота...**")
    exit()


# Команда "prefix"
@app.on_message(filters.me & filters.command("prefix", prefixes="."))
def change_prefix_command(command, message):
    if len(message.command) > 1:
        new_prefix = message.command[1]
        change_prefix(new_prefix)
        message.edit_text("Ваш префикс изменён. Перезапустите юзербота командой *off*, чтобы префикс изменился.")
    elif command.startswith(".prefix"):
        with open("userbot.info", "r") as file:
            prefix = file.readlines()[3].strip()
        message.edit_text(f"**Ваш префикс:\n{prefix}**")


def is_allowed(user_id):
    with open("userbot.info", "r") as file:
        first_line = file.readline()
        return str(user_id) in first_line


def change_prefix(new_prefix):
    with open("userbot.info", "r+") as file:
        lines = file.readlines()
        lines[3] = new_prefix + "\n"
        file.seek(0)
        file.writelines(lines)
        file.truncate()


# Команда "afk"
@app.on_message(filters.me & filters.command("afk", prefixes=prefix_userbot))
def set_afk_mode(_, message):
    global afk_mode, afk_reason, afk_start_time
    afk_mode = True
    afk_reason = " ".join(message.command[1:])
    afk_start_time = datetime.now()
    message.edit_text("**😴AFK-режим включён!**")


@app.on_message(filters.mentioned)
def check_afk(_, message):
    if afk_mode:
        current_time = datetime.now()
        time_diff = current_time - afk_start_time
        message.reply_text(f"**💤Пользователь сейчас в AFK. \nВремя - {time_diff} \nПричина - {afk_reason}**")


# Команда "afkoff"
@app.on_message(filters.me & filters.command("afkoff", prefixes=prefix_userbot))
def unset_afk_mode(_, message):
    global afk_mode
    afk_mode = False
    message.edit_text("**🥱AFK-режим выключен!**")


# Команда "swap"
@app.on_message(filters.command("swap", prefixes=prefix_userbot))
def swap(_, message):
    original_text = message.reply_to_message.text
    swapped_text = swap_layout(original_text)
    message.reply_text(swapped_text)

eng_to_rus = str.maketrans(
    "qwertyuiop[]asdfghjkl;'zxcvbnm,.`",
    "йцукенгшщзхъфывапролджэячсмитьбюё"
)
rus_to_eng = str.maketrans(
    "йцукенгшщзхъфывапролджэячсмитьбюё",
    "qwertyuiop[]asdfghjkl;'zxcvbnm,.`"
)


def swap_layout(text):
    words = text.split()
    swapped_words = []
    for word in words:
        if word.isupper():
            swapped_word = word.lower().translate(rus_to_eng if 'а' <= word.lower()[0] <= 'я' or word.lower()[0] == 'ё' else eng_to_rus)
            swapped_words.append(swapped_word.upper())
        else:
            swapped_words.append(word.translate(rus_to_eng if 'а' <= word.lower()[0] <= 'я' or word.lower()[0] == 'ё' else eng_to_rus))
    return ' '.join(swapped_words)


# Команда "block"
@app.on_message(filters.private & filters.me & filters.command("block", prefixes=prefix_userbot))
def block_user(client, message):
    user_id = message.chat.id
    user_name = message.chat.username
    message.edit(f"**{user_name} заблокирован.**")
    client.block_user(user_id)


print("Юзербот Telery запущен!\nВерсия: 1.8.1\nЕсли есть вопросы, пишите сюда:\nhttps://t.me/TelerySupportBot")
app.run()
