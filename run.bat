@echo off
REM активируем виртуальное окружение Python
call venv\Scripts\activate

REM запускаем python скрипт
python main.py

REM деактивируем виртуальное окружение и завершаем батник
deactivate