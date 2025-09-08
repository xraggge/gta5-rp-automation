@echo off
echo Установка зависимостей для Telegram Game Bot...
echo.

echo Проверка Python...
python --version
if %errorlevel% neq 0 (
    echo ОШИБКА: Python не найден! Установите Python 3.8+ с https://python.org
    pause
    exit /b 1
)

echo.
echo Установка пакетов...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo ОШИБКА: Не удалось установить зависимости!
    pause
    exit /b 1
)

echo.
echo Установка завершена успешно!
echo.
echo Следующие шаги:
echo 1. Получите токен бота у @BotFather в Telegram
echo 2. Замените YOUR_BOT_TOKEN_HERE в main.py на ваш токен
echo 3. Запустите: python main.py
echo.
pause
