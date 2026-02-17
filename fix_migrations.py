"""
اسکریپت برای ساخت و اعمال migration ها
"""
import subprocess
import sys

def run_command(command, description):
    """اجرای یک دستور"""
    print(f"\n{'='*60}")
    print(f"📌 {description}")
    print(f"{'='*60}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True, encoding='utf-8')
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ خطا: {e}")
        if e.stderr:
            print(e.stderr)
        if e.stdout:
            print(e.stdout)
        return False

def main():
    print("\n" + "="*60)
    print("🔧 ساخت و اعمال Migration ها")
    print("="*60)
    
    # ساخت migration ها
    if not run_command("python manage.py makemigrations prompts", "ساخت migration ها"):
        print("⚠️  ممکن است migration ها از قبل وجود داشته باشند")
    
    # اعمال migration ها
    if not run_command("python manage.py migrate", "اعمال migration ها"):
        print("❌ خطا در اعمال migration ها")
        return
    
    print("\n" + "="*60)
    print("✅ Migration ها با موفقیت اعمال شدند!")
    print("="*60)
    print("\n📌 حالا می‌توانید سرور را اجرا کنید:")
    print("   python manage.py runserver")

if __name__ == "__main__":
    main()
