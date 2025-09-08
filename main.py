#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import threading
import random
import cv2
import numpy as np
import pyautogui
import pydirectinput
import keyboard
import mss
from PIL import Image
from io import BytesIO
import telebot
from telebot import types

# Импортируем модули для игровых функций
try:
    from roulette_module import perform_step
    from kachalka_module import run_kachalka, stop_kachalka
    from anti_afk_module import start_anti_afk, stop_anti_afk, is_anti_afk_running
    from tokarka_module import start_tokarka, stop_tokarka, is_tokarka_running
    from number_module import start_number_bot, stop_number_bot, is_number_bot_running, get_available_numbers
    from additional_functions_module import start_additional_functions, stop_additional_functions, is_additional_functions_running, get_available_functions
    print("✅ Все игровые модули загружены успешно")
except ImportError as e:
    print(f"⚠️ Предупреждение: Не удалось загрузить игровые модули: {e}")
    print("Создайте файлы roulette_module.py, kachalka_module.py, anti_afk_module.py, tokarka_module.py, number_module.py, additional_functions_module.py")
    
    # Заглушки для функций
    def perform_step(step, chat_id=None):
        return (step + 1) % 6
    
    def run_kachalka(debug=False):
        print("Качалка не доступна - модуль не найден")
    
    def stop_kachalka():
        print("Качалка не доступна - модуль не найден")
    
    def start_anti_afk():
        print("Анти-афк не доступен - модуль не найден")
        return False
    
    def stop_anti_afk():
        print("Анти-афк не доступен - модуль не найден")
    
    def is_anti_afk_running():
        return False
    
    def start_tokarka(debug=False):
        print("Токарка не доступна - модуль не найден")
        return False
    
    def stop_tokarka():
        print("Токарка не доступна - модуль не найден")
        return False
    
    def is_tokarka_running():
        return False
    
    def start_number_bot(target_number=None, debug=False):
        print("Номера не доступны - модуль не найден")
        return False
    
    def stop_number_bot():
        print("Номера не доступны - модуль не найден")
        return False
    
    def is_number_bot_running():
        return False
    
    def get_available_numbers():
        return []
    
    def start_additional_functions(target_function=None, debug=False):
        print("Дополнительные функции не доступны - модуль не найден")
        return False
    
    def stop_additional_functions():
        print("Дополнительные функции не доступны - модуль не найден")
        return False
    
    def is_additional_functions_running():
        return False
    
    def get_available_functions():
        return []

# Настройки бота (нужно будет указать ваш токен)
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"

# Глобальные переменные
bot = telebot.TeleBot(BOT_TOKEN)
chat_id = None
kachalka_running = False
running_roulette = False
running_afk = False
tokarka_running = False
number_bot_running = False
additional_functions_running = False
kachalka_thread = None

# Направления для анти-афк
DIRECTIONS = ['w', 'a', 's', 'd']

# Изображения (пути к файлам)
IMGFOOD = "food.png"  # Путь к изображению еды

def get_main_keyboard():
    """Создает основную клавиатуру бота с индикаторами состояния (Reply Keyboard)"""
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    
    # Определяем состояние кнопок
    roulette_status = "🟢" if running_roulette else "🔴"
    kachalka_status = "🟢" if kachalka_running else "🔴"
    afk_status = "🟢" if running_afk else "🔴"
    tokarka_status = "🟢" if tokarka_running else "🔴"
    number_status = "🟢" if number_bot_running else "🔴"
    additional_status = "🟢" if additional_functions_running else "🔴"
    
    # Первый ряд - основные функции
    keyboard.row(
        f"{roulette_status} 🎰 Рулетка",
        f"{kachalka_status} 🏋️ Качалка",
        f"{afk_status} 🚫 Анти-афк"
    )
    
    # Второй ряд - новые функции
    keyboard.row(
        f"{tokarka_status} 🔧 Токарка",
        f"{number_status} 🔢 Номера",
        f"{additional_status} ⚙️ Функции"
    )
    
    # Третий ряд - скриншоты
    keyboard.row(
        "📸 Скриншот",
        "📸 Скриншот F10"
    )
    
    # Четвертый ряд - управление
    keyboard.row(
        "⏻ Выключить"
    )
    
    return keyboard

# Функции перенесены в отдельные модули

def start(message):
    """Обработчик команды /start"""
    global chat_id
    chat_id = message.chat.id
    
    welcome_text = (
        "🎮 Добро пожаловать в игрового бота!\n\n"
        "Доступные функции:\n"
        "• 🎰 Рулетка - автоматическая игра в рулетку\n"
        "• 🏋️ Качалка - автоматическая прокачка персонажа\n"
        "• 🚫 Анти-афк - предотвращение отключения за неактивность\n"
        "• 📸 Скриншоты - создание снимков экрана\n\n"
        "Используйте кнопки ниже для управления:"
    )
    
    bot.send_message(chat_id, welcome_text, reply_markup=get_main_keyboard())

def roulette_loop(chat_id):
    """Основной цикл рулетки"""
    step = 0
    
    try:
        while running_roulette:
            step = perform_step(step, chat_id)
            time.sleep(0.5)
    except Exception as e:
        bot.send_message(chat_id, f'Произошла ошибка: {e}. Возврат к пункту 0')
        pydirectinput.press('backspace')
        pydirectinput.press('escape')
        step = 0

# Функция perform_step перенесена в roulette_module.py

def toggle_roulette(message):
    """Переключает состояние рулетки"""
    global running_roulette, chat_id
    chat_id = message.chat.id
    
    # Переключаем состояние
    if not running_roulette:
        running_roulette = True
        threading.Thread(target=roulette_loop, args=(chat_id,), daemon=True).start()
        status_text = "🟢 Рулетка запущена!"
    else:
        running_roulette = False
        status_text = "🔴 Рулетка остановлена."
    
    # Отправляем сообщение о статусе и обновляем клавиатуру
    try:
        # Небольшая задержка для гарантии обновления состояния
        time.sleep(0.1)
        
        # Отправляем сообщение о статусе с обновленной клавиатурой
        bot.send_message(chat_id, status_text, reply_markup=get_main_keyboard())
    except Exception as e:
        print(f"Ошибка отправки сообщения: {e}")
        # Если не удалось отправить, пробуем еще раз
        bot.send_message(chat_id, status_text, reply_markup=get_main_keyboard())

def toggle_anti_afk(message):
    """Переключает состояние анти-афк"""
    global running_afk, chat_id
    chat_id = message.chat.id
    
    # Переключаем состояние
    if not running_afk:
        if start_anti_afk():
            running_afk = True
            status_text = "🟢 Анти-афк запущена!"
        else:
            status_text = "❌ Ошибка запуска анти-афк!"
    else:
        stop_anti_afk()
        running_afk = False
        status_text = "🔴 Анти-афк остановлена."
    
    # Отправляем сообщение о статусе и обновляем клавиатуру
    try:
        # Небольшая задержка для гарантии обновления состояния
        time.sleep(0.1)
        
        # Отправляем сообщение о статусе с обновленной клавиатурой
        bot.send_message(chat_id, status_text, reply_markup=get_main_keyboard())
    except Exception as e:
        print(f"Ошибка отправки сообщения: {e}")
        # Если не удалось отправить, пробуем еще раз
        bot.send_message(chat_id, status_text, reply_markup=get_main_keyboard())

def shutdown_bot(message):
    """Выключает бота"""
    global chat_id
    chat_id = message.chat.id
    
    bot.send_message(chat_id, 'Бот выключается...')
    os._exit(0)

def screenshot_f10(message):
    """Делает скриншот с помощью F10"""
    global chat_id
    chat_id = message.chat.id
    
    try:
        pydirectinput.press('f10')
        time.sleep(0.2)
        screenshot = pyautogui.screenshot()
        
        bio = BytesIO()
        bio.name = 'screenshot.png'
        screenshot.save(bio, 'PNG')
        bio.seek(0)
        
        bot.send_document(chat_id, bio)
        pydirectinput.press('escape')
        bot.send_message(chat_id, '📸 Скриншот F10 сделан и отправлен.')
    except Exception as e:
        bot.send_message(chat_id, f'❌ Ошибка при скриншоте F10: {e}')

def screenshot(message):
    """Делает скриншот всех мониторов"""
    chat_id = message.chat.id
    
    try:
        time.sleep(0.2)
        with mss.mss() as sct:
            img = sct.grab(sct.monitors[0])
            img_pil = Image.frombytes('RGB', img.size, img.rgb)
        
        bio = BytesIO()
        bio.name = 'screenshot.png'
        img_pil.save(bio, 'PNG')
        bio.seek(0)
        
        bot.send_photo(chat_id, bio)
        bot.send_message(chat_id, '📸 Скриншот всех мониторов сделан и отправлен.')
    except Exception as e:
        bot.send_message(chat_id, f'❌ Ошибка при скриншоте: {e}')

def toggle_kachalka(message):
    """Переключает состояние качалки"""
    global kachalka_running, kachalka_thread, chat_id
    chat_id = message.chat.id
    
    # Переключаем состояние
    if not kachalka_running:
        kachalka_running = True
        kachalka_thread = threading.Thread(target=run_kachalka, args=(True,), daemon=True)  # Включаем debug
        kachalka_thread.start()
        status_text = "🟢 Качалка запущена! (Debug окно открыто)"
    else:
        kachalka_running = False
        stop_kachalka()  # Останавливаем качалку через модуль
        kachalka_thread = None
        status_text = "🔴 Качалка остановлена."
    
    # Отправляем сообщение о статусе и обновляем клавиатуру
    try:
        # Небольшая задержка для гарантии обновления состояния
        time.sleep(0.1)
        
        # Отправляем сообщение о статусе с обновленной клавиатурой
        bot.send_message(chat_id, status_text, reply_markup=get_main_keyboard())
    except Exception as e:
        print(f"Ошибка отправки сообщения: {e}")
        # Если не удалось отправить, пробуем еще раз
        bot.send_message(chat_id, status_text, reply_markup=get_main_keyboard())

def toggle_tokarka(message):
    """Переключает состояние токарки"""
    global tokarka_running, chat_id
    chat_id = message.chat.id
    
    if not tokarka_running:
        tokarka_running = True
        start_tokarka(debug=True)  # Запускаем с отладкой
        status_text = "🟢 Токарка запущена!"
    else:
        tokarka_running = False
        stop_tokarka()
        status_text = "🔴 Токарка остановлена."
    
    # Отправляем сообщение о статусе и обновляем клавиатуру
    try:
        # Небольшая задержка для гарантии обновления состояния
        time.sleep(0.1)
        
        # Отправляем сообщение о статусе с обновленной клавиатурой
        bot.send_message(chat_id, status_text, reply_markup=get_main_keyboard())
    except Exception as e:
        print(f"Ошибка отправки сообщения: {e}")
        # Если не удалось отправить, пробуем еще раз
        bot.send_message(chat_id, status_text, reply_markup=get_main_keyboard())

def toggle_number_bot(message):
    """Переключает состояние бота номеров"""
    global number_bot_running, chat_id
    chat_id = message.chat.id
    
    if not number_bot_running:
        number_bot_running = True
        start_number_bot(debug=True)  # Запускаем с отладкой
        status_text = "🟢 Бот номеров запущен!"
    else:
        number_bot_running = False
        stop_number_bot()
        status_text = "🔴 Бот номеров остановлен."
    
    # Отправляем сообщение о статусе и обновляем клавиатуру
    try:
        # Небольшая задержка для гарантии обновления состояния
        time.sleep(0.1)
        
        # Отправляем сообщение о статусе с обновленной клавиатурой
        bot.send_message(chat_id, status_text, reply_markup=get_main_keyboard())
    except Exception as e:
        print(f"Ошибка отправки сообщения: {e}")
        # Если не удалось отправить, пробуем еще раз
        bot.send_message(chat_id, status_text, reply_markup=get_main_keyboard())

def toggle_additional_functions(message):
    """Переключает состояние дополнительных функций"""
    global additional_functions_running, chat_id
    chat_id = message.chat.id
    
    if not additional_functions_running:
        additional_functions_running = True
        start_additional_functions(debug=True)  # Запускаем с отладкой
        status_text = "🟢 Дополнительные функции запущены!"
    else:
        additional_functions_running = False
        stop_additional_functions()
        status_text = "🔴 Дополнительные функции остановлены."
    
    # Отправляем сообщение о статусе и обновляем клавиатуру
    try:
        # Небольшая задержка для гарантии обновления состояния
        time.sleep(0.1)
        
        # Отправляем сообщение о статусе с обновленной клавиатурой
        bot.send_message(chat_id, status_text, reply_markup=get_main_keyboard())
    except Exception as e:
        print(f"Ошибка отправки сообщения: {e}")
        # Если не удалось отправить, пробуем еще раз
        bot.send_message(chat_id, status_text, reply_markup=get_main_keyboard())

# Обработчики команд
@bot.message_handler(commands=['start'])
def handle_start(message):
    start(message)

# Обработчик текстовых сообщений (для Reply Keyboard)
@bot.message_handler(func=lambda message: message.text and not message.text.startswith('/'))
def handle_text(message):
    text = message.text
    
    if "🎰 Рулетка" in text:
        toggle_roulette(message)
    elif "🏋️ Качалка" in text:
        toggle_kachalka(message)
    elif "🚫 Анти-афк" in text:
        toggle_anti_afk(message)
    elif "🔧 Токарка" in text:
        toggle_tokarka(message)
    elif "🔢 Номера" in text:
        toggle_number_bot(message)
    elif "⚙️ Функции" in text:
        toggle_additional_functions(message)
    elif "📸 Скриншот" in text and "F10" not in text:
        screenshot(message)
    elif "📸 Скриншот F10" in text:
        screenshot_f10(message)
    elif "⏻ Выключить" in text:
        shutdown_bot(message)
    else:
        # Если сообщение не распознано, показываем меню
        bot.send_message(message.chat.id, "Выберите действие:", reply_markup=get_main_keyboard())

if __name__ == "__main__":
    print("Запуск бота...")
    print("Не забудьте указать BOT_TOKEN в коде!")
    
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE" or BOT_TOKEN == "123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789":
        print("ОШИБКА: Не указан токен бота!")
        print("Получите токен у @BotFather в Telegram и замените YOUR_BOT_TOKEN_HERE на ваш токен")
        sys.exit(1)
    
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(f"Ошибка при запуске бота: {e}")
