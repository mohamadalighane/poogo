@echo off
chcp 65001 >nul
echo ============================================================
echo 🔧 ساخت و اعمال Migration ها
echo ============================================================
echo.

echo 📊 ساخت migration ها...
python manage.py makemigrations prompts

echo.
echo 💾 اعمال migration ها به دیتابیس...
python manage.py migrate

echo.
echo ✅ Migration ها با موفقیت اعمال شدند!
echo.
echo 📌 حالا می‌توانید سرور را اجرا کنید:
echo    python manage.py runserver
echo.
pause
