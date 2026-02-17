@echo off
chcp 65001 >nul
echo ============================================================
echo 🚀 راه‌اندازی Poogo
echo ============================================================
echo.

echo 📦 نصب وابستگی‌ها...
python -m pip install Django>=4.2.0 Pillow>=10.0.0 django-crispy-forms>=2.0 crispy-bootstrap5>=0.7

echo.
echo 📊 ساخت migration ها...
python manage.py makemigrations

echo.
echo 💾 اعمال migration ها...
python manage.py migrate

echo.
echo ✅ آماده است!
echo.
echo 📌 برای ساخت کاربر ادمین:
echo    python manage.py createsuperuser
echo.
echo 📌 برای ایجاد داده‌های نمونه:
echo    python manage.py create_sample_data
echo.
echo 📌 برای اجرای سرور:
echo    python manage.py runserver
echo.
pause
