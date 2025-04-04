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

print("Бот працює...")

# Токен бота и ID чата администратора
TOKEN = "7747992449:AAEqWIUYRlhbdiwUnXqCYV3ODpNX9VUsed8"
CHAT_ID = "2045410830"  # ID администратора

# Глобальный список предопределённых номеров заказа (10 000 номеров)
order_numbers = ["№" + str(i).zfill(5) for i in range(1, 10001)]
# Список всех заказов (в памяти)
orders_list = []

def get_next_order_number():
    global order_numbers
    if order_numbers:
        return order_numbers.pop(0)
    else:
        return None

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
    
    web_app_url = "https://applabua.github.io/Septic24service/?user_id=" + str(user.id)
    keyboard = [[InlineKeyboardButton("Замовити послугу♻️", web_app=WebAppInfo(url=web_app_url))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    photo_url = "https://i.ibb.co/BH3bjrPP/IMG-9356.jpg"
    if update.message:
        await update.message.reply_photo(photo=photo_url, caption=greeting_text, reply_markup=reply_markup)

# Команда /showorders – показать все заказы (только для администратора)
async def show_orders(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.id != int(CHAT_ID):
        await update.message.reply_text("У вас немає доступу до перегляду замовлень.")
        return
    if not orders_list:
        await update.message.reply_text("Поки що немає жодного замовлення.")
    else:
        # Собираем все заказы в один текст
        all_orders = "\n\n".join(orders_list)
        await update.message.reply_text(all_orders)

# Обработчик данных, отправленных через Telegram.WebApp.sendData
async def webapp_data_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.web_app_data:
        data_str = update.web_app_data.data
        try:
            order = json.loads(data_str)
        except Exception:
            order = {}
        
        # Получаем следующий номер заказа из предопределённого списка
        assigned_number = get_next_order_number()
        if not assigned_number:
            await context.bot.send_message(chat_id=update.effective_user.id, text="Вибачте, більше немає вільних номерів замовлень.")
            return
        
        # Формируем текст заказа
        finalMsg = f"{assigned_number}\nНове замовлення від Septic24:\n"
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

        if order.get('user_id'):
            finalMsg += f"UserID: {order.get('user_id')}\n"

        # Сохраняем заказ в глобальном списке
        orders_list.append(finalMsg)
        
        # Отправляем заказ администратору
        await context.bot.send_message(chat_id=CHAT_ID, text=finalMsg)

        # Вычисляем бонус по номеру заказа
        try:
            num = int(assigned_number[1:])
        except Exception:
            num = 0
        if num % 5 == 0:
            bonus_text = "Ваше замовлення 5/5 ✅\nЗнижка 10% 🎉"
        else:
            bonus = num % 5
            bonus_text = f"Ваше замовлення {bonus}/5 ✅\nЗнижка 2% 💧"
        try:
            if str(order.get('user_id')).isdigit():
                await context.bot.send_message(chat_id=int(order.get('user_id')), text=bonus_text)
        except Exception:
            pass

        if update.effective_message:
            await update.effective_message.reply_text("Ваше замовлення збережено!\nОчікуйте на дзвінок.")

        print("Отримано замовлення:", finalMsg)

def main() -> None:
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("showorders", show_orders))
    application.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, webapp_data_handler))
    application.run_polling()

if __name__ == "__main__":
    main()
