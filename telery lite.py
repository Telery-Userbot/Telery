from pyrogram import Client, filters
import importlib
from datetime import datetime, timedelta
import time

with open("userbot.info", "r") as file:
    lines = file.readlines()
    api_id = int(lines[0].strip())
    api_hash = lines[1].strip()
    prefix_userbot = lines[2].strip()

app = Client("telery_userbot", api_id=api_id, api_hash=api_hash)
start_time = time.time()


def load_modules():
    modules = []
    with open("modules.info", "r") as file:
        for line in file:
            module_name = line.strip()
            module = importlib.import_module(module_name)
            modules.append((module.cinfo, module.ccomand))
    return modules


@app.on_message(filters.me & filters.command("help", prefixes=prefix_userbot))
async def help_command(client, message):
    modules = load_modules()
    prefix = prefix_userbot
    help_text = "**Модулей загружено: {}**\n".format(len(modules))
    for cinfo, ccomand in modules:
        help_text += f"{cinfo} - {ccomand}\n"
    help_text += (f"**Стандартные команды:**\n"
                  f"ℹ`{prefix_userbot}info` - инфо о юзерботе\n"
                  f"⌛`{prefix}ping` - Пишет пинг юб.\n"
                  f"💤`{prefix}off` - Отключает юзербота.")
    await message.reply_text(help_text)


@app.on_message(filters.me & filters.command("info", prefixes=prefix_userbot))
async def info_command(_, message):
    current_time = time.time()
    uptime_seconds = int(round(current_time - start_time))
    uptime = str(timedelta(seconds=uptime_seconds))
    ping_start_time = time.time()
    await message.delete()
    ping_end_time = time.time()
    ping_time = round((ping_end_time - ping_start_time) * 1000, 1)
    user = message.from_user
    username = f"[{user.first_name} {user.last_name}](https://t.me/{user.username})"
    await app.send_photo(
        chat_id=message.chat.id,
        photo="https://user-images.githubusercontent.com/149149385/278584536-1dab252e-9fd4-4a0c-a80e-5e16c1220eaa.jpg",
        caption=f"**✨Telery**\n"
                f"__🔧Version: 2.0__\n"
                f"Source: @telery_userbot2\n"
                f"**Dev-version💜**\n"
                f"**Ping: {ping_time}ms**\n"
                f"**Uptime: {uptime}**\n"
                f"User: {username}"
    )


@app.on_message(filters.me & filters.command(["off"], prefixes=prefix_userbot))
def turn_off(_, message):
    message.edit("**💤Отключаю юзербота...**")
    exit()


@app.on_message(filters.me & filters.command(["ping"], prefixes=prefix_userbot))
def ping(_, message):
    ping_start_time = time.time()
    msg = message.edit("🌕")
    ping_end_time = time.time()
    ping_time = round((ping_end_time - ping_start_time) * 1000)
    uptime_seconds = int(round(time.time() - start_time))
    uptime = str(timedelta(seconds=uptime_seconds))
    msg.edit(f"**🕛Ваш пинг: {ping_time} мс**\n**Uptime: {uptime}**")


def load_and_exec_modules():
    with open("modules.info", "r") as file:
        for line in file:
            module_name = line.strip()
            module = importlib.import_module(module_name)
            if hasattr(module, 'register_math_commands'):
                module.register_math_commands(app)

load_and_exec_modules()

print("Основа Telery запущена! Версия Telery: 2.0. Тех. поддержка: https://t.me/TelerySupportBot")
app.run()
