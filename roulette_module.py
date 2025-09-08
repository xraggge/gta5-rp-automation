#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль для автоматической игры в рулетку
"""

import time
import random
import pyautogui
import pydirectinput
from PIL import Image
import cv2
import numpy as np

class RouletteBot:
    def __init__(self):
        self.step = 0
        self.running = False
        self.bet_amount = 100  # Сумма ставки
        self.bet_type = "red"  # Тип ставки: red, black, green, number
        
    def perform_step(self, step, chat_id=None):
        """Выполняет один шаг рулетки"""
        try:
            if step == 0:
                # Шаг 0: Открыть меню рулетки
                self.open_roulette_menu()
                return 1
                
            elif step == 1:
                # Шаг 1: Выбрать тип ставки
                self.select_bet_type()
                return 2
                
            elif step == 2:
                # Шаг 2: Установить сумму ставки
                self.set_bet_amount()
                return 3
                
            elif step == 3:
                # Шаг 3: Сделать ставку
                self.place_bet()
                return 4
                
            elif step == 4:
                # Шаг 4: Дождаться результата
                self.wait_for_result()
                return 5
                
            elif step == 5:
                # Шаг 5: Забрать выигрыш или начать заново
                self.collect_winnings()
                return 0  # Начать заново
                
            else:
                return 0
                
        except Exception as e:
            print(f"Ошибка в шаге {step}: {e}")
            return 0
    
    def open_roulette_menu(self):
        """Открывает меню рулетки"""
        # Нажимаем клавишу для открытия меню (например, R)
        pydirectinput.press('r')
        time.sleep(1)
        
        # Ищем изображение рулетки на экране
        try:
            location = pyautogui.locateOnScreen('roulette.png', confidence=0.8)
            if location:
                center = pyautogui.center(location)
                pyautogui.click(center)
                time.sleep(0.5)
        except:
            print("Не удалось найти изображение рулетки")
    
    def select_bet_type(self):
        """Выбирает тип ставки"""
        # Случайный выбор типа ставки
        bet_types = ["red", "black", "green"]
        self.bet_type = random.choice(bet_types)
        
        # Кликаем по соответствующей области
        if self.bet_type == "red":
            # Клик по красной области
            pyautogui.click(400, 300)
        elif self.bet_type == "black":
            # Клик по черной области
            pyautogui.click(500, 300)
        elif self.bet_type == "green":
            # Клик по зеленой области (0)
            pyautogui.click(450, 250)
        
        time.sleep(0.5)
    
    def set_bet_amount(self):
        """Устанавливает сумму ставки"""
        # Кликаем по полю ввода суммы
        pyautogui.click(600, 400)
        time.sleep(0.2)
        
        # Очищаем поле
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.1)
        
        # Вводим сумму ставки
        pyautogui.typewrite(str(self.bet_amount))
        time.sleep(0.5)
    
    def place_bet(self):
        """Делает ставку"""
        # Кликаем по кнопке "Поставить"
        pyautogui.click(700, 500)
        time.sleep(1)
    
    def wait_for_result(self):
        """Ждет результата рулетки"""
        # Ждем завершения вращения
        time.sleep(5)
        
        # Можно добавить логику для определения результата
        # по изображению или другим способом
        pass
    
    def collect_winnings(self):
        """Забирает выигрыш"""
        # Кликаем по кнопке "Забрать" или "Новая игра"
        pyautogui.click(700, 500)
        time.sleep(1)
        
        # Обновляем сумму ставки (может увеличить при выигрыше)
        if random.random() < 0.3:  # 30% шанс увеличить ставку
            self.bet_amount = min(self.bet_amount * 1.5, 1000)
        else:
            self.bet_amount = max(self.bet_amount * 0.8, 50)

# Глобальный экземпляр бота рулетки
roulette_bot = RouletteBot()

def perform_step(step, chat_id=None):
    """Главная функция для выполнения шага рулетки"""
    return roulette_bot.perform_step(step, chat_id)
