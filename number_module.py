#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль для работы с номерами - автоматическое распознавание и клик по номерам
"""

import cv2
import numpy as np
import pyautogui
import pydirectinput
import time
import threading
import os
from typing import Optional, Tuple, List

class NumberBot:
    """Класс для автоматической работы с номерами"""
    
    def __init__(self):
        self.running = False
        self.thread = None
        self.number_images = {}
        self.confidence = 0.8
        self.load_number_images()
        
    def load_number_images(self):
        """Загружает все изображения номеров"""
        for i in range(1, 21):  # number_1.jpg до number_20.jpg
            filename = f"number_{i}.jpg"
            if os.path.exists(filename):
                self.number_images[i] = filename
                print(f"✅ Загружен номер {i}: {filename}")
            else:
                print(f"⚠️ Не найден номер {i}: {filename}")
    
    def find_number(self, number: int) -> Optional[Tuple[int, int, int, int]]:
        """Ищет конкретный номер на экране"""
        if number not in self.number_images:
            print(f"Изображение для номера {number} не найдено")
            return None
        
        try:
            location = pyautogui.locateOnScreen(
                self.number_images[number], 
                confidence=self.confidence
            )
            if location:
                return (location.left, location.top, location.width, location.height)
        except Exception as e:
            print(f"Ошибка поиска номера {number}: {e}")
        return None
    
    def find_any_number(self) -> Optional[Tuple[int, int, int, int, int]]:
        """Ищет любой номер на экране и возвращает его значение и позицию"""
        for number, filename in self.number_images.items():
            try:
                location = pyautogui.locateOnScreen(
                    filename, 
                    confidence=self.confidence
                )
                if location:
                    return (number, location.left, location.top, location.width, location.height)
            except Exception as e:
                continue
        return None
    
    def click_number(self, location: Tuple[int, int, int, int]) -> bool:
        """Кликает по номеру"""
        try:
            # Вычисляем центр изображения
            center_x = location[0] + location[2] // 2
            center_y = location[1] + location[3] // 2
            
            # Кликаем по центру
            pydirectinput.click(center_x, center_y)
            time.sleep(0.5)
            return True
        except Exception as e:
            print(f"Ошибка клика по номеру: {e}")
            return False
    
    def click_specific_number(self, number: int) -> bool:
        """Кликает по конкретному номеру"""
        location = self.find_number(number)
        if location:
            return self.click_number(location)
        else:
            print(f"Номер {number} не найден на экране")
            return False
    
    def click_any_number(self) -> Optional[int]:
        """Кликает по любому найденному номеру и возвращает его значение"""
        result = self.find_any_number()
        if result:
            number, x, y, w, h = result
            location = (x, y, w, h)
            if self.click_number(location):
                return number
        return None
    
    def run_number_loop(self, target_number: Optional[int] = None, debug: bool = False):
        """Основной цикл работы с номерами"""
        print(f"🔢 Запуск цикла номеров (цель: {target_number or 'любой'})...")
        
        while self.running:
            try:
                if target_number:
                    # Ищем конкретный номер
                    location = self.find_number(target_number)
                    if location:
                        if debug:
                            print(f"Найден номер {target_number} в позиции: {location}")
                        
                        if self.click_number(location):
                            print(f"✅ Кликнул по номеру {target_number}")
                            time.sleep(1)
                    else:
                        if debug:
                            print(f"Номер {target_number} не найден")
                else:
                    # Ищем любой номер
                    result = self.find_any_number()
                    if result:
                        number, x, y, w, h = result
                        if debug:
                            print(f"Найден номер {number} в позиции: ({x}, {y}, {w}, {h})")
                        
                        if self.click_number((x, y, w, h)):
                            print(f"✅ Кликнул по номеру {number}")
                            time.sleep(1)
                    else:
                        if debug:
                            print("Номера не найдены")
                
                # Пауза между циклами
                time.sleep(2)
                
            except Exception as e:
                print(f"Ошибка в цикле номеров: {e}")
                time.sleep(1)
        
        print("🛑 Цикл номеров остановлен")
    
    def start(self, target_number: Optional[int] = None, debug: bool = False):
        """Запускает работу с номерами"""
        if self.running:
            print("Работа с номерами уже запущена")
            return False
        
        self.running = True
        self.thread = threading.Thread(
            target=self.run_number_loop, 
            args=(target_number, debug),
            daemon=True
        )
        self.thread.start()
        print(f"✅ Работа с номерами запущена (цель: {target_number or 'любой'})")
        return True
    
    def stop(self):
        """Останавливает работу с номерами"""
        if not self.running:
            print("Работа с номерами не запущена")
            return False
        
        self.running = False
        if self.thread:
            self.thread.join(timeout=2)
        print("🛑 Работа с номерами остановлена")
        return True
    
    def is_running(self) -> bool:
        """Проверяет, запущена ли работа с номерами"""
        return self.running
    
    def get_available_numbers(self) -> List[int]:
        """Возвращает список доступных номеров"""
        return list(self.number_images.keys())
    
    def test_all_numbers(self) -> dict:
        """Тестирует поиск всех номеров"""
        results = {}
        for number in self.get_available_numbers():
            location = self.find_number(number)
            results[number] = location is not None
        return results

# Глобальный экземпляр бота
number_bot = NumberBot()

def start_number_bot(target_number: Optional[int] = None, debug: bool = False) -> bool:
    """Запускает работу с номерами"""
    return number_bot.start(target_number, debug)

def stop_number_bot() -> bool:
    """Останавливает работу с номерами"""
    return number_bot.stop()

def is_number_bot_running() -> bool:
    """Проверяет, запущена ли работа с номерами"""
    return number_bot.is_running()

def click_number(number: int) -> bool:
    """Кликает по конкретному номеру"""
    return number_bot.click_specific_number(number)

def click_any_number() -> Optional[int]:
    """Кликает по любому найденному номеру"""
    return number_bot.click_any_number()

def get_available_numbers() -> List[int]:
    """Возвращает список доступных номеров"""
    return number_bot.get_available_numbers()

def test_numbers() -> dict:
    """Тестирует поиск всех номеров"""
    return number_bot.test_all_numbers()

if __name__ == "__main__":
    # Тестирование модуля
    print("🔢 Тестирование модуля номеров...")
    
    # Показываем доступные номера
    available = get_available_numbers()
    print(f"📋 Доступные номера: {available}")
    
    # Тестируем поиск номеров
    print("\n🔍 Тестирование поиска номеров:")
    results = test_numbers()
    for number, found in results.items():
        status = "✅" if found else "❌"
        print(f"{status} Номер {number}: {'найден' if found else 'не найден'}")
    
    # Тестируем поиск любого номера
    print("\n🎯 Поиск любого номера:")
    result = number_bot.find_any_number()
    if result:
        number, x, y, w, h = result
        print(f"✅ Найден номер {number} в позиции: ({x}, {y}, {w}, {h})")
    else:
        print("ℹ️ Номера не найдены (это нормально, если игра не запущена)")
    
    print("\n🎯 Модуль номеров готов к использованию")
