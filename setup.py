"""
اسکریپت راه‌اندازی خودکار Poogo
"""
import os
import sys
import subprocess

def run_command(command, description):
    """اجرای یک دستور و نمایش نتیجه"""
    print(f"\n{'='*60}")
    print(f"📌 {description}")
    print(f"{'='*60}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ خطا: {e}")
        if e.stderr:
            print(e.stderr)
        return False

def main():
    print("\n" + "="*60)
    print("🚀 راه‌اندازی Poogo - پلتفرم پیشرفته پرامت‌ها")
    print("="*60)
    
    # بررسی Python
    print(f"\n✅ Python version: {sys.version}")
    
    # مرحله 1: نصب وابستگی‌ها
    print("\n" + "="*60)
    print("مرحله 1: نصب وابستگی‌ها")
    print("="*60)
    
    packages = [
        "Django>=4.2.0",
        "Pillow>=10.0.0",
        "django-crispy-forms>=2.0",
        "crispy-bootstrap5>=0.7"
    ]
    
    for package in packages:
        if not run_command(f'python -m pip install "{package}"', f"نصب {package}"):
            print(f"⚠️  هشدار: نصب {package} با مشکل مواجه شد")
    
    # مرحله 2: ساخت migration ها
    print("\n" + "="*60)
    print("مرحله 2: ساخت migration ها")
    print("="*60)
    
    if not run_command("python manage.py makemigrations", "ساخت migration ها"):
        print("⚠️  ممکن است migration ها از قبل وجود داشته باشند")
    
    # مرحله 3: اعمال migration ها
    print("\n" + "="*60)
    print("مرحله 3: اعمال migration ها به دیتابیس")
    print("="*60)
    
    if not run_command("python manage.py migrate", "اعمال migration ها"):
        print("❌ خطا در اعمال migration ها")
        return
    
    # مرحله 4: ساخت کاربر ادمین
    print("\n" + "="*60)
    print("مرحله 4: ساخت کاربر ادمین")
    print("="*60)
    print("⚠️  برای ساخت کاربر ادمین، دستور زیر را دستی اجرا کنید:")
    print("   python manage.py createsuperuser")
    
    # مرحله 5: ایجاد داده‌های نمونه
    print("\n" + "="*60)
    print("مرحله 5: ایجاد داده‌های نمونه")
    print("="*60)
    print("⚠️  برای ایجاد داده‌های نمونه، دستور زیر را اجرا کنید:")
    print("   python manage.py create_sample_data")
    
    # مرحله 6: راه‌اندازی سرور
    print("\n" + "="*60)
    print("✅ راه‌اندازی کامل شد!")
    print("="*60)
    print("\n📌 برای اجرای سرور، دستور زیر را بزنید:")
    print("   python manage.py runserver")
    print("\n🌐 سپس به آدرس زیر بروید:")
    print("   http://127.0.0.1:8000")
    print("\n🔐 پنل ادمین:")
    print("   http://127.0.0.1:8000/admin")
    print("\n" + "="*60)

if __name__ == "__main__":
    main()
