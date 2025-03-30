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
import threading

from flask import Flask, request, jsonify

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo, Bot
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
)

print("Бот працює...")

# Токен бота и ID чата администратора
TOKEN = "7747992449:AAEqWIUYRlhbdiwUnXqCYV3ODpNX9VUsed8"
CHAT_ID = "2045410830"  # ID администратора

# Глобальный объект бота
bot = Bot(token=TOKEN)

# Функция для генерации глобального номера заказа (единая нумерация)
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

# Flask-приложение для обработки POST-запросов с заказами
flask_app = Flask(__name__)

@flask_app.route('/save_order', methods=['POST'])
def save_order():
    data = request.get_json()
    order_text = data.get("order", "")
    if not order_text:
        return jsonify({"status": "error", "error": "No order provided"}), 400
    # Генерируем глобальный номер заказа
    order_number = get_next_order_number()
    formatted_order_number = "№" + str(order_number).zfill(5)
    # Если заказ уже содержит номер, удаляем его
    lines = order_text.split("\n")
    if lines and lines[0].startswith("№"):
        lines.pop(0)
    final_order_text = f"{formatted_order_number}\n" + "\n".join(lines)
    
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("orders.txt", "a", encoding="utf-8") as f:
        f.write(f"[{now_str}]\n{final_order_text}\n\n")
    
    try:
        bot.send_message(chat_id=CHAT_ID, text=final_order_text)
    except Exception as e:
        print("Error sending order to Telegram:", e)
    
    return jsonify({"status": "ok", "order_number": formatted_order_number})

# Обработчик команды /start – отправляем пользователю кнопку для открытия WebApp
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
        formatted_order_number = "№" + str(order_number).zfill(5)
        
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

        bonus = order_number % 5
        if bonus == 0:
            bonus = 5
        bonus_text = (
            f"Ваше замовлення {bonus}/5 ✅\n"
            "Знижка 2% 💧, Кожне 5 замовлення – знижка 10% 🎉"
        )
        try:
            if user_id_str.isdigit():
                await context.bot.send_message(chat_id=int(user_id_str), text=bonus_text)
        except Exception:
            pass

        if update.effective_message:
            await update.effective_message.reply_text("Ваше замовлення збережено!\nОчікуйте на дзвінок.")

        print("Отримано замовлення:", finalMsg)

# Функция для локального запуска Flask-сервера (используется только при запуске в режиме --run-both)
def run_flask():
    port = int(os.environ.get("PORT", 5000))
    flask_app.run(host="0.0.0.0", port=port)

# Функция для запуска Telegram-бота (polling)
def main() -> None:
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("orders", orders_history))
    application.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, webapp_data_handler))
    application.run_polling()

if __name__ == "__main__":
    # Если запущено с параметром --bot-only, запускаем только бота
    if "--bot-only" in sys.argv:
        main()
    # Если указано --run-both, запускаем оба сервиса в одном процессе (для локального тестирования)
    elif "--run-both" in sys.argv:
        threading.Thread(target=run_flask, daemon=True).start()
        main()
    else:
        # По умолчанию ничего не запускаем, чтобы при импорте (например, Gunicorn) не стартовал встроенный сервер.
        # Gunicorn подхватит переменную flask_app для обслуживания веб-запросов.
        pass
