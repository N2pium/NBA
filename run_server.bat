@echo off
echo Starting NBA Website Server...
call .venv\Scripts\activate.bat
cd website
python manage.py runserver
pause
