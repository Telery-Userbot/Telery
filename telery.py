from pyrogram import Client, filters
import importlib
import sys
import time
import requests
from datetime import timedelta
import os

with open("userbot.info", "r") as file:
    lines = file.readlines()
    api_id = int(lines[0].strip())
    api_hash = lines[1].strip()
    prefix_userbot = lines[2].strip()

app = Client("telery_userbot", api_id=api_id, api_hash=api_hash)
start_time = time.time()
loaded_modules = {}
waiting_for_confirmation = {}


def reload_modules():
    global loaded_modules
    modules_to_reload = list(loaded_modules.keys())
    loaded_modules.clear()
    for module_name in modules_to_reload:
        try:
            if module_name in sys.modules:
                module = importlib.reload(sys.modules[module_name])
            else:
                module = importlib.import_module(module_name)
            loaded_modules[module_name] = module
        except Exception as e:
            print(f"Ошибка перезагрузки модуля {module_name}: {e}")
    for module in loaded_modules.values():
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if callable(attr) and (attr_name.startswith("register_") or attr_name.startswith("command_")):
                try:
                    attr(app)
                except Exception as e:
                    print(f"Ошибка вызова функции {attr_name} из модуля {module.__name__}: {e}")


def load_modules():
    global loaded_modules
    modules = []
    loaded_modules.clear()
    with open("modules.info", "r") as file:
        for line in file:
            module_name = line.strip()
            if module_name:
                try:
                    if module_name in sys.modules:
                        module = importlib.reload(sys.modules[module_name])
                    else:
                        module = importlib.import_module(module_name)
                    loaded_modules[module_name] = module
                    modules.append(module)
                except Exception as e:
                    print(f"Ошибка загрузки модуля {module_name}: {e}")
    return modules


def load_and_exec_modules():
    modules = load_modules()
    for module in modules:
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if callable(attr) and (attr_name.startswith("register_") or attr_name.startswith("command_")):
                try:
                    attr(app)
                except Exception as e:
                    print(f"Ошибка вызова функции {attr_name} из модуля {module.__name__}: {e}")


@app.on_message(filters.me & filters.command(["help"], prefixes=prefix_userbot))
async def help_command(_, message):
    prefix = prefix_userbot
    help_text = "**⚙Модулей загружено: {}**\n".format(len(loaded_modules))
    for module_name, module in loaded_modules.items():
        cinfo = module.cinfo if isinstance(module.cinfo, tuple) else (module.cinfo,)
        ccomand = module.ccomand if isinstance(module.ccomand, tuple) else (module.ccomand,)
        for info, command in zip(cinfo, ccomand):
            help_text += f"{info} - {command}\n"
    help_text += (f"**Стандартные команды:**\n"
                  f"ℹ`{prefix}info` - инфо о юзерботе\n"
                  f"⌛`{prefix}ping` - Пишет пинг юб.\n"
                  f"💤`{prefix}off` - Отключает юзербота.\n"
                  "`.prefix` - Изменяет префикс юзербота. Стандартный префикс: `.`\n"
                  f"`{prefix}md` - Установить модуль из гитхаба. Канал с модулями: @telery_modules2\n"
                  f"`{prefix}restart` - Перезагрузить все модули.")
    await message.edit_text(help_text)


@app.on_message(filters.me & filters.command(["info"], prefixes=prefix_userbot))
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
                f"__🔧Version: 2.1__\n"
                f"Source: @telery_userbot2\n"
                f"**Classic version❤**\n"
                f"**Ping: {ping_time}ms**\n"
                f"**Uptime: {uptime}**\n"
                f"User: {username}"
    )


@app.on_message(filters.me & filters.command(["off"], prefixes=prefix_userbot))
async def turn_off(_, message):
    await message.edit("**💤Отключаю юзербота...**")
    exit()


@app.on_message(filters.me & filters.command(["ping"], prefixes=prefix_userbot))
async def ping(_, message):
    ping_start_time = time.time()
    msg = await message.edit("🌕")
    ping_end_time = time.time()
    ping_time = round((ping_end_time - ping_start_time) * 1000)
    uptime_seconds = int(round(time.time() - start_time))
    uptime = str(timedelta(seconds=uptime_seconds))
    await msg.edit(f"**🕛Ваш пинг: {ping_time} мс**\n**Uptime: {uptime}**")


@app.on_message(filters.me & filters.command(["restart"], prefixes=prefix_userbot))
async def restart(_, message):
    await message.edit("**Перезапускаю модули...**")
    restart_start_time = time.time()
    reload_modules()
    restart_end_time = time.time()
    restart_time = round(restart_end_time - restart_start_time, 2)
    await message.edit(f"**Модули перезапущены. Это заняло {restart_time} секунд.**")


@app.on_message(filters.me & filters.command(["prefix"], prefixes="."))
async def change_prefix_command(_, message):
    if len(message.command) > 1:
        new_prefix = message.command[1]
        change_prefix(new_prefix)
        await message.edit_text("Ваш префикс изменён. Перезапустите юзербота командой `off`, чтобы префикс изменился.")
    elif message.text.startswith(".prefix"):
        with open("userbot.info", "r") as file:
            prefix = file.readlines()[2].strip()
        await message.edit_text(f"**Ваш префикс:\n{prefix}**")


@app.on_message(filters.me & filters.command(["md"], prefixes=prefix_userbot))
async def search_module(_, message):
    if len(message.command) > 1:
        module_name = message.command[1]
        repo_url = f"https://api.github.com/search/repositories?q=telerymodule_{module_name}"
        response = requests.get(repo_url)
        data = response.json()

        if data["total_count"] > 0:
            repo = data["items"][0]
            repo_full_name = repo["full_name"]
            repo_size = repo["size"]
            repo_updated = repo["updated_at"]
            repo_author = repo["owner"]["login"]
            await message.edit(f"**Модуль {module_name} найден:**\n"
                               f"**👨Автор:** {repo_author}\n"
                               f"**📁Размер файла:** {repo_size} KB\n"
                               f"**🔃Обновлено:** {repo_updated}\n"
                               f"**Установить?** Y/N")
            waiting_for_confirmation[message.from_user.id] = (repo_full_name, module_name, message)
        else:
            await message.edit(f"**⛔Модуль с именем {module_name} не найден.**")
    else:
        await message.edit("Пожалуйста, укажите название модуля.")


@app.on_message(filters.me & filters.text)
async def handle_response(_, response_message):
    user_id = response_message.from_user.id
    if user_id in waiting_for_confirmation:
        repo_full_name, module_name, original_message = waiting_for_confirmation.pop(user_id)
        if response_message.text.upper() == 'Y':
            file_url = f"https://raw.githubusercontent.com/{repo_full_name}/main/module_{module_name}.py"
            file_response = requests.get(file_url)

            if file_response.status_code == 200:
                with open(f"module_{module_name}.py", "wb") as file:
                    file.write(file_response.content)
                with open("modules.info", "a") as file:
                    file.write(f"\nmodule_{module_name}\n")
                await original_message.edit(f"**✅Модуль `{module_name}` успешно установлен.**")
            else:
                await original_message.edit(f"**⛔Не удалось найти файл module_{module_name}.py в репозитории.**")
        else:
            await original_message.edit("**Установка модуля отменена.**")

load_and_exec_modules()
print("Основа Telery запущена! Версия Telery: 2.1. Тех. поддержка: https://t.me/TelerySupportBot")
app.run()
