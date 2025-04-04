import pytz
import tzlocal
# Переопределяем tzlocal.get_localzone, чтобы возвращался pytz-объект
tzlocal.get_localzone = lambda: pytz.timezone("Europe/Kiev")

def patched_astimezone(tz):
    if tz is None:
        return None
    if not isinstance(tz, pytz.BaseTzInfo):
        try:
            if isinstance(tz, str):
                return pytz.timezone(tz)
            if hasattr(tz, 'key'):
                return pytz.timezone(tz.key)
            return pytz.timezone(str(tz))
        except Exception as e:
            raise TypeError('Only timezones from the pytz library are supported') from e
    return tz

import apscheduler.util
apscheduler.util.astimezone = patched_astimezone

import logging
import sys
import json
from datetime import datetime

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
)

import asyncio
import os
from aiohttp import web

print("Бот працює...")

# Токен бота и ID чата администратора
TOKEN = "7747992449:AAEqWIUYRlhbdiwUnXqCYV3ODpNX9VUsed8"
CHAT_ID = "2045410830"  # ID администратора

# Словарь для бонус-счётчиков (не сохраняется между перезапусками)
bonus_counters = {}

# Функция для генерации глобального номера заказа на сервере
def get_next_order_number():
    try:
        with open("last_order_number.txt", "r", encoding="utf-8") as f:
            last_order = int(f.read().strip())
    except Exception:
        last_order = 0
    last_order += 1
    with open("last_order_number.txt", "w", encoding="utf-8") as f:
        f.write(str(last_order))
    return last_order

# Команда /start – отправляем пользователю кнопку для открытия WebApp
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{now}] Користувач {user.full_name} (ID: {user.id}) викликав /start")

    greeting_text = (
        "👋 Ласкаво просимо до Septic24!\n\n"
        "Ми надаємо професійні послуги з викачування вигрібних ям, септиків, каналізацій "
        "та вуличних туалетів по всій Україні.\n\n"
        "Натисніть кнопку нижче, щоб відкрити міні‑додаток і оформити замовлення:"
    )
    
    # URL веб‑приложения на GitHub Pages, с передачей user_id
    web_app_url = "https://applabua.github.io/Septic24service/?user_id=" + str(user.id)
    keyboard = [[InlineKeyboardButton("Замовити послугу♻️", web_app=WebAppInfo(url=web_app_url))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    photo_url = "https://i.ibb.co/BH3bjrPP/IMG-9356.jpg"
    if update.message:
        await update.message.reply_photo(photo=photo_url, caption=greeting_text, reply_markup=reply_markup)

# Команда /orders – показать содержимое файла orders.txt (только для администратора)
async def orders_history(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.id != int(CHAT_ID):
        await update.message.reply_text("У вас немає доступу до історії замовлень.")
        return
    try:
        with open("orders.txt", "r", encoding="utf-8") as f:
            content = f.read()
        if not content.strip():
            content = "Історія замовлень порожня."
    except FileNotFoundError:
        content = "Файл з історією замовлень не знайдено."
    await update.message.reply_text(content)

# Обработчик данных, отправленных через Telegram.WebApp.sendData
async def webapp_data_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.web_app_data:
        data_str = update.web_app_data.data
        try:
            order = json.loads(data_str)
        except Exception:
            order = {}

        # Генерируем глобальный номер заказа
        order_number = get_next_order_number()
        formatted_order_number = "№" + str(order_number).zfill(5)
        
        # Формируем текст заказа для администратора с номером заказа
        finalMsg = f"{formatted_order_number}\nНове замовлення від Septic24:\n"
        finalMsg += f"Ім'я: {order.get('name','')}\n"
        finalMsg += f"Телефон: {order.get('phone','')}\n"
        finalMsg += f"Область: {order.get('region','')}\n"
        finalMsg += f"Адреса: {order.get('address','')}\n"
    
        serviceIndex = order.get('serviceIndex')
        if serviceIndex is not None:
            servicesTitles = [
                "Викачка вигрібних ям",
                "Викачка мулу чи піску",
                "Викачка септика",
                "Прочистка труб",
                "Викачка туалету"
            ]
            if 0 <= serviceIndex < len(servicesTitles):
                finalMsg += f"Послуга: {servicesTitles[serviceIndex]}\n"
            if serviceIndex == 3:
                finalMsg += f"Довжина труб: {order.get('length','?')} м\n"
                finalMsg += f"Діаметр труб: {order.get('diameter','?')} мм\n"
            else:
                finalMsg += f"Об'єм ємності: {order.get('volume','?')} м³\n"
                finalMsg += f"Відстань від парковки до ємності: {order.get('distance','?')} м\n"
        
        coords = order.get('coords')
        if coords and 'x' in coords and 'y' in coords:
            lat = coords['y']
            lon = coords['x']
            finalMsg += f"Геолокація: {lat:.5f}, {lon:.5f}\n"
            finalMsg += f"OpenStreetMap: https://www.openstreetmap.org/?mlat={lat}&mlon={lon}\n"

        user_id_str = order.get('user_id','')
        if user_id_str:
            finalMsg += f"UserID: {user_id_str}\n"

        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("orders.txt", "a", encoding="utf-8") as f:
            f.write(f"[{now_str}]\n{finalMsg}\n\n")

        await context.bot.send_message(chat_id=CHAT_ID, text=finalMsg)

        # Определяем бонус и скидку
        if order_number % 5 == 0:
            bonus_text = f"Ваше замовлення 5/5 ✅\nЗнижка 10% 🎉"
        else:
            bonus_text = f"Ваше замовлення {order_number % 5}/5 ✅\nЗнижка 2% 💧"
        try:
            if user_id_str.isdigit():
                await context.bot.send_message(chat_id=int(user_id_str), text=bonus_text)
        except Exception:
            pass

        if update.effective_message:
            await update.effective_message.reply_text("Ваше замовлення збережено!\nОчікуйте на дзвінок.")

        print("Отримано замовлення:", finalMsg)

# HTTP-эндпоинт для сохранения заказа (используется WebApp)
async def save_order(request):
    try:
        data = await request.json()
        order_text = data.get("order", "")
        # Если в тексте заказа уже есть номер (первая строка начинается с "№"), удаляем её
        lines = order_text.splitlines()
        if lines and lines[0].startswith("№"):
            lines = lines[1:]
        # Генерируем глобальный номер заказа
        order_number = get_next_order_number()
        formatted_order_number = "№" + str(order_number).zfill(5)
        finalMsg = formatted_order_number + "\n" + "\n".join(lines)
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("orders.txt", "a", encoding="utf-8") as f:
            f.write(f"[{now_str}]\n{finalMsg}\n\n")
        # Определяем скидку и бонус
        discount = 10 if order_number % 5 == 0 else 2
        bonus_count = 5 if order_number % 5 == 0 else order_number % 5
        response_data = {
            "status": "ok",
            "order_number": formatted_order_number,
            "discount": discount,
            "bonus": bonus_count,
            "order_text": finalMsg
        }
        # Отправляем заказ админу через Telegram
        await request.app['bot'].bot.send_message(chat_id=CHAT_ID, text=finalMsg)
        return web.json_response(response_data)
    except Exception as e:
        return web.json_response({"status": "error", "error": str(e)})

# Асинхронная функция для запуска бота и HTTP-сервера вместе
async def main():
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("orders", orders_history))
    application.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, webapp_data_handler))
    
    # Создаём приложение aiohttp и добавляем маршрут для /save_order
    app = web.Application()
    app.router.add_post("/save_order", save_order)
    # Чтобы в save_order можно было обращаться к объекту бота
    app['bot'] = application
    
    # Запускаем HTTP-сервер (порт берётся из переменной окружения PORT, иначе 8080)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    print(f"HTTP server started on port {port}")
    
    # Запускаем polling Telegram-бота (будет работать параллельно)
    await application.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
