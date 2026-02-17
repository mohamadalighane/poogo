from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    """دسته‌بندی اصلی پرامت‌ها"""
    name = models.CharField(max_length=100, verbose_name="نام دسته")
    slug = models.SlugField(unique=True, allow_unicode=True, verbose_name="اسلاگ")
    description = models.TextField(blank=True, verbose_name="توضیحات")
    icon = models.CharField(max_length=50, blank=True, verbose_name="آیکون (emoji یا class)")
    color = models.CharField(max_length=7, default="#00d4aa", verbose_name="رنگ")
    order = models.IntegerField(default=0, verbose_name="ترتیب نمایش")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)


class SubCategory(models.Model):
    """زیردسته‌بندی برای دسته‌بندی پیشرفته‌تر"""
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories', verbose_name="دسته اصلی")
    name = models.CharField(max_length=100, verbose_name="نام زیردسته")
    slug = models.SlugField(allow_unicode=True, verbose_name="اسلاگ")
    order = models.IntegerField(default=0, verbose_name="ترتیب")

    class Meta:
        verbose_name = "زیردسته"
        verbose_name_plural = "زیردسته‌ها"
        ordering = ['order', 'name']
        unique_together = ['category', 'slug']

    def __str__(self):
        return f"{self.category.name} > {self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)


class Tag(models.Model):
    """تگ‌ها برای جستجو و فیلتر پیشرفته"""
    name = models.CharField(max_length=50, unique=True, verbose_name="نام تگ")
    slug = models.SlugField(unique=True, allow_unicode=True, verbose_name="اسلاگ")
    color = models.CharField(max_length=7, default="#7c5cff", verbose_name="رنگ")

    class Meta:
        verbose_name = "تگ"
        verbose_name_plural = "تگ‌ها"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)


class Prompt(models.Model):
    """مدل اصلی پرامت"""
    DIFFICULTY_CHOICES = [
        ('beginner', 'مبتدی'),
        ('intermediate', 'متوسط'),
        ('advanced', 'پیشرفته'),
    ]

    LANGUAGE_CHOICES = [
        ('fa', 'فارسی'),
        ('en', 'English'),
        ('both', 'هر دو'),
    ]

    title = models.CharField(max_length=200, verbose_name="عنوان")
    slug = models.SlugField(unique=True, allow_unicode=True, verbose_name="اسلاگ")
    content = models.TextField(verbose_name="متن پرامت")
    description = models.TextField(blank=True, verbose_name="توضیحات کوتاه")
    
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='prompts', verbose_name="دسته‌بندی")
    subcategory = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='prompts', verbose_name="زیردسته")
    tags = models.ManyToManyField(Tag, blank=True, related_name='prompts', verbose_name="تگ‌ها")
    
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='beginner', verbose_name="سطح دشواری")
    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES, default='fa', verbose_name="زبان")
    
    # آمار و تعامل
    views_count = models.IntegerField(default=0, verbose_name="تعداد بازدید")
    likes_count = models.IntegerField(default=0, verbose_name="تعداد لایک")
    copies_count = models.IntegerField(default=0, verbose_name="تعداد کپی")
    
    # متا
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='prompts', verbose_name="نویسنده")
    is_featured = models.BooleanField(default=False, verbose_name="ویژه")
    is_published = models.BooleanField(default=True, verbose_name="منتشر شده")
    is_premium = models.BooleanField(default=False, verbose_name="پریمیوم")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="آخرین بروزرسانی")
    published_at = models.DateTimeField(null=True, blank=True, verbose_name="تاریخ انتشار")

    class Meta:
        verbose_name = "پرامت"
        verbose_name_plural = "پرامت‌ها"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-views_count']),
            models.Index(fields=['-created_at']),
            models.Index(fields=['is_published', 'is_featured']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        if self.is_published and not self.published_at:
            from django.utils import timezone
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('prompt_detail', kwargs={'slug': self.slug})

    def increment_views(self):
        self.views_count += 1
        self.save(update_fields=['views_count'])

    def increment_copies(self):
        self.copies_count += 1
        self.save(update_fields=['copies_count'])


class PromptExample(models.Model):
    """مثال‌های استفاده از پرامت"""
    prompt = models.ForeignKey(Prompt, on_delete=models.CASCADE, related_name='examples', verbose_name="پرامت")
    input_text = models.TextField(verbose_name="ورودی نمونه")
    output_text = models.TextField(verbose_name="خروجی نمونه")
    order = models.IntegerField(default=0, verbose_name="ترتیب")

    class Meta:
        verbose_name = "مثال"
        verbose_name_plural = "مثال‌ها"
        ordering = ['order']

    def __str__(self):
        return f"مثال برای {self.prompt.title}"


class PromptCollection(models.Model):
    """مجموعه‌های پرامت (مثل مجموعه‌های آموزشی)"""
    name = models.CharField(max_length=200, verbose_name="نام مجموعه")
    slug = models.SlugField(unique=True, allow_unicode=True, verbose_name="اسلاگ")
    description = models.TextField(blank=True, verbose_name="توضیحات")
    prompts = models.ManyToManyField(Prompt, related_name='collections', verbose_name="پرامت‌ها")
    is_featured = models.BooleanField(default=False, verbose_name="ویژه")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "مجموعه"
        verbose_name_plural = "مجموعه‌ها"
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)
