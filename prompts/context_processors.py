from .models import Category


def categories(request):
    """اضافه کردن دسته‌بندی‌ها به همه template ها"""
    return {
        'categories': Category.objects.filter(is_active=True)[:10]
    }
