#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль токарки - автоматическая работа с токарным станком
"""

import cv2
import numpy as np
import pyautogui
import pydirectinput
import time
import threading
from typing import Optional, Tuple

class TokarkaBot:
    """Класс для автоматической работы с токарным станком"""
    
    def __init__(self):
        self.running = False
        self.thread = None
        self.tokarka_image = "Tokarka.png"
        self.confidence = 0.8
        
    def find_tokarka(self) -> Optional[Tuple[int, int, int, int]]:
        """Ищет токарный станок на экране"""
        try:
            location = pyautogui.locateOnScreen(
                self.tokarka_image, 
                confidence=self.confidence
            )
            if location:
                return (location.left, location.top, location.width, location.height)
        except Exception as e:
            print(f"Ошибка поиска токарки: {e}")
        return None
    
    def click_tokarka(self, location: Tuple[int, int, int, int]) -> bool:
        """Кликает по токарному станку"""
        try:
            # Вычисляем центр изображения
            center_x = location[0] + location[2] // 2
            center_y = location[1] + location[3] // 2
            
            # Кликаем по центру
            pydirectinput.click(center_x, center_y)
            time.sleep(0.5)
            return True
        except Exception as e:
            print(f"Ошибка клика по токарке: {e}")
            return False
    
    def start_work(self) -> bool:
        """Начинает работу с токарным станком"""
        try:
            # Ищем токарку
            location = self.find_tokarka()
            if not location:
                print("Токарный станок не найден на экране")
                return False
            
            # Кликаем по токарке
            if not self.click_tokarka(location):
                return False
            
            # Нажимаем клавиши для начала работы
            pydirectinput.press('e')  # Взаимодействие
            time.sleep(0.5)
            pydirectinput.press('space')  # Подтверждение
            time.sleep(0.5)
            
            print("Работа с токарным станком начата")
            return True
            
        except Exception as e:
            print(f"Ошибка начала работы с токаркой: {e}")
            return False
    
    def stop_work(self) -> bool:
        """Останавливает работу с токарным станком"""
        try:
            # Нажимаем Escape для выхода
            pydirectinput.press('escape')
            time.sleep(0.5)
            
            print("Работа с токарным станком остановлена")
            return True
            
        except Exception as e:
            print(f"Ошибка остановки работы с токаркой: {e}")
            return False
    
    def run_tokarka_loop(self, debug: bool = False):
        """Основной цикл работы токарки"""
        print("🔄 Запуск цикла токарки...")
        
        while self.running:
            try:
                # Ищем токарку
                location = self.find_tokarka()
                
                if location:
                    if debug:
                        print(f"Токарка найдена в позиции: {location}")
                    
                    # Проверяем, нужно ли начать работу
                    # Здесь можно добавить логику проверки состояния
                    
                    # Нажимаем E для взаимодействия
                    pydirectinput.press('e')
                    time.sleep(1)
                    
                    # Нажимаем пробел для подтверждения
                    pydirectinput.press('space')
                    time.sleep(2)
                    
                else:
                    if debug:
                        print("Токарка не найдена, ожидание...")
                
                # Пауза между циклами
                time.sleep(3)
                
            except Exception as e:
                print(f"Ошибка в цикле токарки: {e}")
                time.sleep(1)
        
        print("🛑 Цикл токарки остановлен")
    
    def start(self, debug: bool = False):
        """Запускает токарку"""
        if self.running:
            print("Токарка уже запущена")
            return False
        
        self.running = True
        self.thread = threading.Thread(
            target=self.run_tokarka_loop, 
            args=(debug,),
            daemon=True
        )
        self.thread.start()
        print("✅ Токарка запущена")
        return True
    
    def stop(self):
        """Останавливает токарку"""
        if not self.running:
            print("Токарка не запущена")
            return False
        
        self.running = False
        if self.thread:
            self.thread.join(timeout=2)
        print("🛑 Токарка остановлена")
        return True
    
    def is_running(self) -> bool:
        """Проверяет, запущена ли токарка"""
        return self.running

# Глобальный экземпляр бота
tokarka_bot = TokarkaBot()

def start_tokarka(debug: bool = False) -> bool:
    """Запускает токарку"""
    return tokarka_bot.start(debug)

def stop_tokarka() -> bool:
    """Останавливает токарку"""
    return tokarka_bot.stop()

def is_tokarka_running() -> bool:
    """Проверяет, запущена ли токарка"""
    return tokarka_bot.is_running()

def run_tokarka(debug: bool = False):
    """Запускает токарку (для совместимости)"""
    return start_tokarka(debug)

if __name__ == "__main__":
    # Тестирование модуля
    print("🔧 Тестирование модуля токарки...")
    
    # Проверяем наличие изображения
    import os
    if os.path.exists("Tokarka.png"):
        print("✅ Изображение Tokarka.png найдено")
    else:
        print("❌ Изображение Tokarka.png не найдено")
    
    # Тестируем поиск токарки
    location = tokarka_bot.find_tokarka()
    if location:
        print(f"✅ Токарка найдена в позиции: {location}")
    else:
        print("ℹ️ Токарка не найдена (это нормально, если игра не запущена)")
    
    print("🎯 Модуль токарки готов к использованию")
