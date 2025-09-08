#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль для автоматической качалки персонажа
"""

import time
import cv2
import numpy as np
import pyautogui
import pydirectinput
import keyboard
from PIL import Image
import mss

class KachalkaBot:
    def __init__(self):
        self.running = False
        self.debug = False
        self.screen_w, self.screen_h = pyautogui.size()
        
        # Определяем координаты в зависимости от разрешения
        if self.screen_w > 2000 and self.screen_h > 1100:
            self.x1, self.y1, self.x2, self.y2 = 1100, 950, 1450, 1300
            print("Использую координаты для 1920x1080+")
        else:
            self.x1, self.y1, self.x2, self.y2 = 775, 567, 1128, 949
            print("Использую координаты для меньших разрешений")
        
        self.region = (self.x1, self.y1, self.x2, self.y2)
        self.threshold = 5
        self.green_radius_offset = 6
        self.inside = False
        self.last_e_press = 0
        self.last_food_check = 0
        
        # Настройки для поиска еды
        self.food_images = ['food.png', 'food_1.png']
        self.food_confidence = 0.85
        
    def capture_screen(self, region):
        """Захватывает экран в указанной области"""
        with mss.mss() as sct:
            screenshot = sct.grab(region)
            img = Image.frombytes('RGB', screenshot.size, screenshot.rgb)
            return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    
    def find_image(self, template_path, confidence=0.8):
        """Ищет изображение на экране"""
        try:
            location = pyautogui.locateOnScreen(template_path, confidence=confidence)
            if location:
                return pyautogui.center(location)
            return None
        except:
            return None
    
    def get_circle(self, frame, lower_color, upper_color):
        """Находит круг на изображении по цвету"""
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_color, upper_color)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            if cv2.contourArea(largest_contour) > 100:
                (x, y), radius = cv2.minEnclosingCircle(largest_contour)
                return int(x), int(y), int(radius)
        
        return None
    
    def check_food(self):
        """Проверяет наличие еды на экране"""
        for food_img in self.food_images:
            food_loc = self.find_image(food_img, confidence=self.food_confidence)
            if food_loc:
                print(f"Найдена еда: {food_img}")
                return True
        return False
    
    def eat_food(self):
        """Использует еду"""
        print("Используем еду...")
        keyboard.press_and_release('0')
        time.sleep(1)
        keyboard.press_and_release('e')
        self.last_e_press = time.time()
    
    def press_e(self):
        """Нажимает клавишу E"""
        keyboard.press_and_release('e')
        self.last_e_press = time.time()
    
    def run_kachalka(self, debug=False):
        """Основная функция качалки"""
        self.running = True
        self.debug = debug
        
        print("Качалка запущена!")
        if debug:
            print("Debug окно будет открыто")
        
        # Нажимаем E для начала
        self.press_e()
        
        try:
            while self.running:
                now = time.time()
                
                # Проверяем еду каждые 120 секунд
                if now - self.last_food_check >= 120:
                    self.last_food_check = now
                    if self.check_food():
                        self.eat_food()
                
                # Нажимаем E каждые 15 секунд
                if now - self.last_e_press >= 15:
                    self.press_e()
                
                # Захватываем экран
                frame = self.capture_screen(self.region)
                
                # Ищем белый и зеленый круги
                white_circle = self.get_circle(frame, np.array([0, 0, 200]), np.array([180, 30, 255]))
                green_circle = self.get_circle(frame, np.array([40, 50, 50]), np.array([80, 255, 255]))
                
                if white_circle and green_circle:
                    xw, yw, rw = white_circle
                    xg, yg, rg = green_circle
                    
                    # Увеличиваем радиус зеленого круга
                    rg = max(1, rg + self.green_radius_offset)
                    
                    # Вычисляем расстояние между центрами
                    dist = np.sqrt((xw - xg)**2 + (yw - yg)**2)
                    
                    # Проверяем, нужно ли нажать пробел
                    if dist < rg - rw + self.threshold and not self.inside:
                        time.sleep(0.1)
                        keyboard.send('space')
                        self.inside = True
                        print(f"Нажат пробел! Расстояние: {dist:.2f}")
                    elif dist >= rg - rw + self.threshold:
                        self.inside = False
                    
                    # Отладочная информация
                    if self.debug:
                        cv2.circle(frame, (xw, yw), rw, (255, 255, 255), 2)
                        cv2.circle(frame, (xg, yg), rg, (0, 255, 0), 2)
                        cv2.line(frame, (xw, yw), (xg, yg), (0, 0, 255), 1)
                        cv2.putText(frame, f'dist={int(dist)}', (10, 30), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                
                # Показываем отладочное окно
                if self.debug:
                    cv2.imshow('Debug window - Качалка', frame)
                    key = cv2.waitKey(1) & 0xFF
                    if key == 27:  # ESC для выхода
                        print("ESC нажат - останавливаем качалку")
                        self.running = False
                
                # Небольшая задержка для снижения нагрузки на CPU
                time.sleep(0.01)
        
        except Exception as e:
            print(f"Ошибка в качалке: {e}")
        
        finally:
            # Всегда закрываем окна при выходе
            if self.debug:
                cv2.destroyAllWindows()
                print("Debug окно закрыто")
            print("Качалка остановлена!")
    
    def stop(self):
        """Останавливает качалку"""
        self.running = False

# Глобальный экземпляр бота качалки
kachalka_bot = KachalkaBot()

def run_kachalka(debug=False):
    """Главная функция для запуска качалки"""
    kachalka_bot.run_kachalka(debug)

def stop_kachalka():
    """Останавливает качалку"""
    kachalka_bot.stop()
