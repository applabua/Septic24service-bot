import os
import asyncio
import pytz
import tzlocal
import logging
import sys
import json
from datetime import datetime

# Настраиваем tzlocal для Europe/Kiev
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

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

from aiohttp import web

print("Бот працює...")

# --- Настройки ---
TOKEN = "7747992449:AAEqWIUYRlhbdiwUnXqCYV3ODpNX9VUsed8"  # Замените на ваш токен бота
CHAT_ID = "2045410830"            # Замените на ваш ID администратора

# Словарь для бонус-счётчиков (не сохраняется между перезапусками)
bonus_counters = {}

# Функция для получения следующего глобального номера заказа
def get_next_order_number():
    try:
        with open("order_counter.txt", "r", encoding="utf-8") as f:
            num = int(f.read().strip())
    except FileNotFoundError:
        num = 0
    num += 1
    with open("order_counter.txt", "w", encoding="utf-8") as f:
        f.write(str(num))
    return num

# ===================== Хендлеры Telegram ======================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Команда /start – отправка кнопки с WebApp."""
    user = update.effective_user
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{now}] Користувач {user.full_name} (ID: {user.id}) викликав /start")

    greeting_text = (
        "👋 Ласкаво просимо до Septic24!\n\n"
        "Ми надаємо професійні послуги з викачування вигрібних ям, септиків, каналізацій "
        "та вуличних туалетів по всій Україні.\n\n"
        "Натисніть кнопку нижче, щоб відкрити міні‑додаток і оформити замовлення:"
    )
    
    web_app_url = "https://applabua.github.io/Septic24service/?user_id=" + str(user.id)
    keyboard = [[InlineKeyboardButton("Замовити послугу♻️", web_app=WebAppInfo(url=web_app_url))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    photo_url = "https://i.ibb.co/BH3bjrPP/IMG-9356.jpg"
    if update.message:
        await update.message.reply_photo(photo=photo_url, caption=greeting_text, reply_markup=reply_markup)

async def orders_history(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Команда /orders – показать историю заказов (только для админа)."""
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

async def webapp_data_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик данных, полученных через Telegram.WebApp.sendData()."""
    if update.web_app_data:
        data_str = update.web_app_data.data
        try:
            order = json.loads(data_str)
        except Exception:
            order = {}

        # Получаем глобальный номер заказа
        order_number = get_next_order_number()

        # Формируем текст заказа
        finalMsg = "Нове замовлення від Septic24:\n"
        finalMsg += f"Номер замовлення: {order_number}\n"
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

        # Отправляем заказ админу
        await context.bot.send_message(chat_id=CHAT_ID, text=finalMsg)

        # Бонус-счётчик
        if user_id_str.isdigit():
            uid = int(user_id_str)
            bonus_counters[uid] = bonus_counters.get(uid, 0) + 1
            if bonus_counters[uid] > 5:
                bonus_counters[uid] = 1
            bonus_msg = (
                f"Дякуємо, Ваше замовлення сформовано, очікуйте на дзвінок\n"
                f"Замовлення {bonus_counters[uid]} / 5 ✅\n"
                "Кожне 5 замовлення знижка 10%\n"
                "Ваша знижка 2%\n"
                f"Номер замовлення: {order_number}"
            )
            try:
                await context.bot.send_message(chat_id=uid, text=bonus_msg)
            except Exception:
                pass

        if update.effective_message:
            await update.effective_message.reply_text(
                f"Дякуємо, Ваше замовлення сформовано, очікуйте на дзвінок\n"
                f"Замовлення {bonus_counters.get(int(user_id_str), 1)} / 5 ✅\n"
                "Кожне 5 замовлення знижка 10%\n"
                "Ваша знижка 2%\n"
                f"Номер замовлення: {order_number}"
            )

        print("Отримано замовлення:", finalMsg)

# ======== Эндпоинт /save_order ========
async def save_order(request):
    """Обработчик POST-запроса /save_order, который приходит из HTML."""
    try:
        data = await request.json()
        order_text = data.get("order", "")
        order_number = get_next_order_number()
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        order_entry = f"[{now_str}] Номер замовлення: {order_number}\n{order_text}\n\n"
        with open("orders.txt", "a", encoding="utf-8") as f:
            f.write(order_entry)
        return web.json_response({"status": "success", "order_number": order_number})
    except Exception as e:
        return web.json_response({"status": "error", "error": str(e)}, status=500)

# ======== Настройки AIOHTTP + Bot ========
async def on_startup(app: web.Application) -> None:
    """Запускается автоматически при старте aiohttp-сервера."""
    print("on_startup: создаём Telegram-приложение…")
    application = ApplicationBuilder().token(TOKEN).build()
    app["telegram_app"] = application

    # Регистрируем хендлеры
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("orders", orders_history))
    application.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, webapp_data_handler))

    # Инициализируем приложение бота
    await application.initialize()

    # Запускаем polling как фоновую асинхронную задачу
    asyncio.create_task(application.start_polling())
    print("Бот запущен в фоне (polling).")

async def on_cleanup(app: web.Application) -> None:
    """Вызывается автоматически при завершении aiohttp-сервера."""
    print("on_cleanup: останавливаем Telegram-приложение…")
    application = app["telegram_app"]
    await application.shutdown()
    await application.post_shutdown()
    print("Бот остановлен.")

def create_app() -> web.Application:
    """Создаёт и возвращает aiohttp-приложение со всеми эндпоинтами."""
    http_app = web.Application()
    http_app.router.add_post('/save_order', save_order)
    http_app.on_startup.append(on_startup)
    http_app.on_cleanup.append(on_cleanup)
    return http_app

def main():
    """Главная точка входа – запускает aiohttp на Heroku."""
    port = int(os.environ.get("PORT", 8000))
    app = create_app()
    web.run_app(app, port=port)

if __name__ == "__main__":
    main()
