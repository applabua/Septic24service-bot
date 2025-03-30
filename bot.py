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
import os
from datetime import datetime

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
)

# Дополнительный импорт для создания HTTP-сервера
import asyncio
from aiohttp import web

print("Бот працює...")

# Токен бота и ID администратора
TOKEN = "7747992449:AAEqWIUYRlhbdiwUnXqCYV3ODpNX9VUsed8"
CHAT_ID = "2045410830"  # ID администратора

# Словарь для бонус-счётчиков (не сохраняется между перезапусками)
bonus_counters = {}

# Функция для генерации глобального номера заказа
def get_next_order_number():
    order_file = "order_number.txt"
    if os.path.exists(order_file):
        try:
            with open(order_file, "r", encoding="utf-8") as f:
                last_number = int(f.read().strip())
        except Exception:
            last_number = 0
    else:
        last_number = 0
    new_number = last_number + 1
    with open(order_file, "w", encoding="utf-8") as f:
        f.write(str(new_number))
    return f"№{new_number:05d}"

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
    
    # URL веб-приложения с передачей user_id
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

        order_number = get_next_order_number()
        finalMsg = f"Нове замовлення {order_number} від Septic24:\n"
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
            finalMsg += f"Довжина труб: {order.get('length','?')} м\n"
            finalMsg += f"Діаметр труб: {order.get('diameter','?')} мм\n"

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

        if user_id_str.isdigit():
            uid = int(user_id_str)
            bonus_counters[uid] = bonus_counters.get(uid, 0) + 1
            if bonus_counters[uid] > 5:
                bonus_counters[uid] = 1
            bonus_text = (
                f"Ваше замовлення: {bonus_counters[uid]} / 5 ✅\n"
                "Рухаємось до бонусу! Кожне замовлення наближає вас до ще більшої вигоди 🎯\n\n"
                "💧 На всі замовлення діє знижка 2% — бо ми цінуємо кожного клієнта.\n"
                "🌟 А вже на п’ятому замовленні — даруємо 10% знижки!\n\n"
                "Накопичуйте замовлення, а ми подбаємо про чистоту та ваш комфорт.\n"
                "Septic24 — коли все працює чітко і з турботою 💙"
            )
            try:
                await context.bot.send_message(chat_id=uid, text=bonus_text)
            except Exception:
                pass

        if update.effective_message:
            await update.effective_message.reply_text("Ваше замовлення збережено!\nОчікуйте на дзвінок.")

        print("Отримано замовлення:", finalMsg)

# HTTP-эндпоинт для сохранения заказа (вызывается из WebApp)
async def save_order(request):
    try:
        data = await request.json()
        order_text = data.get("order", "")
        order_number = get_next_order_number()
        order_text = f"Нове замовлення {order_number} від Septic24:\n" + order_text
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("orders.txt", "a", encoding="utf-8") as f:
            f.write(f"[{now_str}]\n{order_text}\n\n")
        # Передаем объект бота в контекст, чтобы отправить сообщение админу
        context: ContextTypes.DEFAULT_TYPE = request.app['context']
        await context.bot.send_message(chat_id=CHAT_ID, text=order_text)
        return web.json_response({"status": "ok", "order_number": order_number})
    except Exception as e:
        return web.json_response({"status": "error", "error": str(e)})

def main() -> None:
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("orders", orders_history))
    application.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, webapp_data_handler))
    
    async def init_aiohttp_app():
        app = web.Application()
        app.add_routes([web.post('/save_order', save_order)])
        # Передаем объект бота в контекст, чтобы иметь доступ к нему из эндпоинта
        app['context'] = application
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, '0.0.0.0', 8080)
        await site.start()
    
    async def main_async():
        await init_aiohttp_app()
        # Запускаем polling Telegram-бота
        await application.run_polling()
    
    # Используем текущий event loop для запуска асинхронного кода
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main_async())

if __name__ == "__main__":
    main()
