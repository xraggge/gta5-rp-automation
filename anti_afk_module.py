#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль для анти-афк (предотвращение отключения за неактивность)
"""

import time
import random
import pydirectinput
import threading

class AntiAFKBot:
    def __init__(self):
        self.running = False
        self.directions = ['w', 'a', 's', 'd']
        self.min_delay = 8
        self.max_delay = 14
        
    def anti_afk_loop(self):
        """Основной цикл анти-афк"""
        print("Анти-афк запущен!")
        
        while self.running:
            # Выбираем случайное направление
            key = random.choice(self.directions)
            
            # Нажимаем клавишу
            pydirectinput.keyDown(key)
            time.sleep(0.01)  # Очень короткое нажатие
            pydirectinput.keyUp(key)
            
            # Случайная задержка между нажатиями
            delay = random.uniform(self.min_delay, self.max_delay)
            time.sleep(delay)
        
        print("Анти-афк остановлен!")
    
    def start(self):
        """Запускает анти-афк"""
        if not self.running:
            self.running = True
            thread = threading.Thread(target=self.anti_afk_loop, daemon=True)
            thread.start()
            return True
        return False
    
    def stop(self):
        """Останавливает анти-афк"""
        self.running = False

# Глобальный экземпляр бота анти-афк
anti_afk_bot = AntiAFKBot()

def start_anti_afk():
    """Запускает анти-афк"""
    return anti_afk_bot.start()

def stop_anti_afk():
    """Останавливает анти-афк"""
    anti_afk_bot.stop()

def is_anti_afk_running():
    """Проверяет, запущен ли анти-афк"""
    return anti_afk_bot.running
