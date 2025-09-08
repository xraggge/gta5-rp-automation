#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль дополнительных функций - работа с изображениями 1.png, 2.png, 3.png, 4.png
"""

import cv2
import numpy as np
import pyautogui
import pydirectinput
import time
import threading
import os
from typing import Optional, Tuple, List, Dict

class AdditionalFunctionsBot:
    """Класс для дополнительных игровых функций"""
    
    def __init__(self):
        self.running = False
        self.thread = None
        self.function_images = {}
        self.confidence = 0.8
        self.load_function_images()
        
    def load_function_images(self):
        """Загружает все изображения функций"""
        # Основные функции
        functions = {
            1: "1.png",
            2: "2.png", 
            3: "3.png",
            4: "4.png",
            "1_1": "1_1.png",
            "2_2": "2_2.png",
            "3_3": "3_3.png"
        }
        
        for func_id, filename in functions.items():
            if os.path.exists(filename):
                self.function_images[func_id] = filename
                print(f"✅ Загружена функция {func_id}: {filename}")
            else:
                print(f"⚠️ Не найдена функция {func_id}: {filename}")
    
    def find_function(self, func_id) -> Optional[Tuple[int, int, int, int]]:
        """Ищет конкретную функцию на экране"""
        if func_id not in self.function_images:
            print(f"Изображение для функции {func_id} не найдено")
            return None
        
        try:
            location = pyautogui.locateOnScreen(
                self.function_images[func_id], 
                confidence=self.confidence
            )
            if location:
                return (location.left, location.top, location.width, location.height)
        except Exception as e:
            print(f"Ошибка поиска функции {func_id}: {e}")
        return None
    
    def find_any_function(self) -> Optional[Tuple[int, int, int, int, int]]:
        """Ищет любую функцию на экране и возвращает её ID и позицию"""
        for func_id, filename in self.function_images.items():
            try:
                location = pyautogui.locateOnScreen(
                    filename, 
                    confidence=self.confidence
                )
                if location:
                    return (func_id, location.left, location.top, location.width, location.height)
            except Exception as e:
                continue
        return None
    
    def click_function(self, location: Tuple[int, int, int, int]) -> bool:
        """Кликает по функции"""
        try:
            # Вычисляем центр изображения
            center_x = location[0] + location[2] // 2
            center_y = location[1] + location[3] // 2
            
            # Кликаем по центру
            pydirectinput.click(center_x, center_y)
            time.sleep(0.5)
            return True
        except Exception as e:
            print(f"Ошибка клика по функции: {e}")
            return False
    
    def click_specific_function(self, func_id) -> bool:
        """Кликает по конкретной функции"""
        location = self.find_function(func_id)
        if location:
            return self.click_function(location)
        else:
            print(f"Функция {func_id} не найдена на экране")
            return False
    
    def click_any_function(self) -> Optional[int]:
        """Кликает по любой найденной функции и возвращает её ID"""
        result = self.find_any_function()
        if result:
            func_id, x, y, w, h = result
            location = (x, y, w, h)
            if self.click_function(location):
                return func_id
        return None
    
    def run_function_loop(self, target_function: Optional[int] = None, debug: bool = False):
        """Основной цикл работы с функциями"""
        print(f"⚙️ Запуск цикла функций (цель: {target_function or 'любая'})...")
        
        while self.running:
            try:
                if target_function:
                    # Ищем конкретную функцию
                    location = self.find_function(target_function)
                    if location:
                        if debug:
                            print(f"Найдена функция {target_function} в позиции: {location}")
                        
                        if self.click_function(location):
                            print(f"✅ Кликнул по функции {target_function}")
                            time.sleep(1)
                    else:
                        if debug:
                            print(f"Функция {target_function} не найдена")
                else:
                    # Ищем любую функцию
                    result = self.find_any_function()
                    if result:
                        func_id, x, y, w, h = result
                        if debug:
                            print(f"Найдена функция {func_id} в позиции: ({x}, {y}, {w}, {h})")
                        
                        if self.click_function((x, y, w, h)):
                            print(f"✅ Кликнул по функции {func_id}")
                            time.sleep(1)
                    else:
                        if debug:
                            print("Функции не найдены")
                
                # Пауза между циклами
                time.sleep(2)
                
            except Exception as e:
                print(f"Ошибка в цикле функций: {e}")
                time.sleep(1)
        
        print("🛑 Цикл функций остановлен")
    
    def start(self, target_function: Optional[int] = None, debug: bool = False):
        """Запускает работу с функциями"""
        if self.running:
            print("Работа с функциями уже запущена")
            return False
        
        self.running = True
        self.thread = threading.Thread(
            target=self.run_function_loop, 
            args=(target_function, debug),
            daemon=True
        )
        self.thread.start()
        print(f"✅ Работа с функциями запущена (цель: {target_function or 'любая'})")
        return True
    
    def stop(self):
        """Останавливает работу с функциями"""
        if not self.running:
            print("Работа с функциями не запущена")
            return False
        
        self.running = False
        if self.thread:
            self.thread.join(timeout=2)
        print("🛑 Работа с функциями остановлена")
        return True
    
    def is_running(self) -> bool:
        """Проверяет, запущена ли работа с функциями"""
        return self.running
    
    def get_available_functions(self) -> List[int]:
        """Возвращает список доступных функций"""
        return list(self.function_images.keys())
    
    def test_all_functions(self) -> Dict[int, bool]:
        """Тестирует поиск всех функций"""
        results = {}
        for func_id in self.get_available_functions():
            location = self.find_function(func_id)
            results[func_id] = location is not None
        return results
    
    def execute_function_sequence(self, sequence: List[int]) -> bool:
        """Выполняет последовательность функций"""
        print(f"🔄 Выполнение последовательности: {sequence}")
        
        for func_id in sequence:
            if not self.running:
                break
                
            print(f"🎯 Выполняю функцию {func_id}")
            if self.click_specific_function(func_id):
                time.sleep(1)
            else:
                print(f"❌ Не удалось выполнить функцию {func_id}")
                return False
        
        print("✅ Последовательность выполнена успешно")
        return True

# Глобальный экземпляр бота
additional_bot = AdditionalFunctionsBot()

def start_additional_functions(target_function: Optional[int] = None, debug: bool = False) -> bool:
    """Запускает работу с дополнительными функциями"""
    return additional_bot.start(target_function, debug)

def stop_additional_functions() -> bool:
    """Останавливает работу с дополнительными функциями"""
    return additional_bot.stop()

def is_additional_functions_running() -> bool:
    """Проверяет, запущена ли работа с дополнительными функциями"""
    return additional_bot.is_running()

def click_function(func_id: int) -> bool:
    """Кликает по конкретной функции"""
    return additional_bot.click_specific_function(func_id)

def click_any_function() -> Optional[int]:
    """Кликает по любой найденной функции"""
    return additional_bot.click_any_function()

def get_available_functions() -> List[int]:
    """Возвращает список доступных функций"""
    return additional_bot.get_available_functions()

def test_functions() -> Dict[int, bool]:
    """Тестирует поиск всех функций"""
    return additional_bot.test_all_functions()

def execute_sequence(sequence: List[int]) -> bool:
    """Выполняет последовательность функций"""
    return additional_bot.execute_function_sequence(sequence)

if __name__ == "__main__":
    # Тестирование модуля
    print("⚙️ Тестирование модуля дополнительных функций...")
    
    # Показываем доступные функции
    available = get_available_functions()
    print(f"📋 Доступные функции: {available}")
    
    # Тестируем поиск функций
    print("\n🔍 Тестирование поиска функций:")
    results = test_functions()
    for func_id, found in results.items():
        status = "✅" if found else "❌"
        print(f"{status} Функция {func_id}: {'найдена' if found else 'не найдена'}")
    
    # Тестируем поиск любой функции
    print("\n🎯 Поиск любой функции:")
    result = additional_bot.find_any_function()
    if result:
        func_id, x, y, w, h = result
        print(f"✅ Найдена функция {func_id} в позиции: ({x}, {y}, {w}, {h})")
    else:
        print("ℹ️ Функции не найдены (это нормально, если игра не запущена)")
    
    print("\n🎯 Модуль дополнительных функций готов к использованию")
