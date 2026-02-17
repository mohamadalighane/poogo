from django.core.management.base import BaseCommand
from prompts.models import Category, SubCategory, Tag, Prompt, PromptExample
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'ایجاد داده‌های نمونه برای تست'

    def handle(self, *args, **options):
        self.stdout.write('در حال ایجاد داده‌های نمونه...')
        
        # ایجاد دسته‌بندی‌ها
        cat_writing = Category.objects.create(
            name='نویسندگی',
            slug='writing',
            description='پرامت‌های مربوط به نویسندگی و تولید محتوا',
            icon='✍️',
            color='#00d4aa'
        )
        
        cat_code = Category.objects.create(
            name='برنامه‌نویسی',
            slug='code',
            description='پرامت‌های برنامه‌نویسی و کدنویسی',
            icon='💻',
            color='#7c5cff'
        )
        
        cat_image = Category.objects.create(
            name='ساخت عکس',
            slug='image-generation',
            description='پرامت‌های ساخت و ویرایش عکس',
            icon='🎨',
            color='#ff5c7c'
        )
        
        cat_education = Category.objects.create(
            name='آموزش',
            slug='education',
            description='پرامت‌های آموزشی',
            icon='📚',
            color='#ffa500'
        )
        
        # ایجاد زیردسته‌ها
        sub_article = SubCategory.objects.create(
            category=cat_writing,
            name='مقاله',
            slug='article'
        )
        
        sub_python = SubCategory.objects.create(
            category=cat_code,
            name='Python',
            slug='python'
        )
        
        # ایجاد تگ‌ها
        tag_seo = Tag.objects.create(name='SEO', slug='seo', color='#00d4aa')
        tag_ai = Tag.objects.create(name='AI', slug='ai', color='#7c5cff')
        tag_design = Tag.objects.create(name='طراحی', slug='design', color='#ff5c7c')
        
        # ایجاد پرامت‌های نمونه
        prompt1 = Prompt.objects.create(
            title='نویسنده مقاله SEO',
            slug='seo-article-writer',
            content='تو یک نویسنده حرفه‌ای SEO هستی. یک مقاله کامل با کلمات کلیدی [موضوع] بنویس، حداقل ۸۰۰ کلمه، با مقدمه جذاب و پاراگراف‌های ساختاریافته.',
            description='نوشتن مقاله SEO حرفه‌ای با ساختار مناسب',
            category=cat_writing,
            subcategory=sub_article,
            difficulty='intermediate',
            tags=[tag_seo],
            is_featured=True,
            is_published=True
        )
        
        prompt2 = Prompt.objects.create(
            title='توضیح کد Python',
            slug='explain-python-code',
            content='این کد Python را خط به خط توضیح بده و بگو هر بخش چه کاری انجام می‌دهد:\n\n```python\n[کد شما]\n```',
            description='توضیح و تحلیل کد Python',
            category=cat_code,
            subcategory=sub_python,
            difficulty='beginner',
            tags=[tag_ai],
            is_published=True
        )
        
        prompt3 = Prompt.objects.create(
            title='ساخت تصویر با AI',
            slug='ai-image-generation',
            content='یک تصویر [توضیحات] با سبک [سبک] و رنگ‌های [رنگ‌ها] بساز. جزئیات: [جزئیات بیشتر]',
            description='ساخت تصویر با AI بر اساس توضیحات',
            category=cat_image,
            difficulty='beginner',
            tags=[tag_ai, tag_design],
            is_featured=True,
            is_published=True
        )
        
        # ایجاد مثال
        PromptExample.objects.create(
            prompt=prompt1,
            input_text='موضوع: بهینه‌سازی سایت',
            output_text='مقاله کامل با مقدمه، بخش‌های مختلف و نتیجه‌گیری...',
            order=1
        )
        
        self.stdout.write(self.style.SUCCESS('داده‌های نمونه با موفقیت ایجاد شدند!'))
        self.stdout.write(f'- {Category.objects.count()} دسته‌بندی')
        self.stdout.write(f'- {SubCategory.objects.count()} زیردسته')
        self.stdout.write(f'- {Tag.objects.count()} تگ')
        self.stdout.write(f'- {Prompt.objects.count()} پرامت')
