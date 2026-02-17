from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Category, SubCategory, Tag, Prompt, PromptExample, PromptCollection


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'color_display', 'order', 'prompt_count', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['order', 'is_active']
    prepopulated_fields = {'slug': ('name',)}
    
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('name', 'slug', 'description')
        }),
        ('ظاهر', {
            'fields': ('icon', 'color', 'order')
        }),
        ('وضعیت', {
            'fields': ('is_active',)
        }),
    )

    def color_display(self, obj):
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 12px; border-radius: 4px;">{}</span>',
            obj.color, obj.color
        )
    color_display.short_description = "رنگ"

    def prompt_count(self, obj):
        count = obj.prompts.count()
        url = reverse('admin:prompts_prompt_changelist') + f'?category__id__exact={obj.id}'
        return format_html('<a href="{}">{} پرامت</a>', url, count)
    prompt_count.short_description = "تعداد پرامت"


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'order', 'prompt_count']
    list_filter = ['category']
    search_fields = ['name', 'category__name']
    list_editable = ['order']
    autocomplete_fields = ['category']

    def prompt_count(self, obj):
        return obj.prompts.count()
    prompt_count.short_description = "تعداد پرامت"


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'color_display', 'prompt_count']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}

    def color_display(self, obj):
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 8px; border-radius: 3px; font-size: 11px;">{}</span>',
            obj.color, obj.color
        )
    color_display.short_description = "رنگ"

    def prompt_count(self, obj):
        return obj.prompts.count()
    prompt_count.short_description = "تعداد پرامت"


class PromptExampleInline(admin.TabularInline):
    model = PromptExample
    extra = 1
    fields = ['input_text', 'output_text', 'order']


@admin.register(Prompt)
class PromptAdmin(admin.ModelAdmin):
    list_display = ['title', 'category_display', 'difficulty_badge', 'views_count', 'likes_count', 'is_featured', 'is_published', 'created_at']
    list_filter = ['category', 'subcategory', 'difficulty', 'language', 'is_featured', 'is_published', 'is_premium', 'tags', 'created_at']
    search_fields = ['title', 'content', 'description', 'tags__name']
    list_editable = ['is_featured', 'is_published']
    prepopulated_fields = {'slug': ('title',)}
    autocomplete_fields = ['category', 'subcategory', 'tags', 'author']
    readonly_fields = ['views_count', 'likes_count', 'copies_count', 'created_at', 'updated_at', 'published_at']
    filter_horizontal = ['tags']
    inlines = [PromptExampleInline]
    
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('title', 'slug', 'content', 'description')
        }),
        ('دسته‌بندی', {
            'fields': ('category', 'subcategory', 'tags')
        }),
        ('ویژگی‌ها', {
            'fields': ('difficulty', 'language', 'is_premium')
        }),
        ('وضعیت', {
            'fields': ('is_featured', 'is_published', 'author')
        }),
        ('آمار', {
            'fields': ('views_count', 'likes_count', 'copies_count'),
            'classes': ('collapse',)
        }),
        ('تاریخ‌ها', {
            'fields': ('created_at', 'updated_at', 'published_at'),
            'classes': ('collapse',)
        }),
    )

    actions = ['make_featured', 'make_unfeatured', 'publish_selected', 'unpublish_selected', 'duplicate_prompts']

    def category_display(self, obj):
        if obj.category:
            color = obj.category.color
            return format_html(
                '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 4px; font-size: 11px;">{}</span>',
                color, obj.category.name
            )
        return "-"
    category_display.short_description = "دسته"

    def difficulty_badge(self, obj):
        colors = {
            'beginner': '#00d4aa',
            'intermediate': '#ffa500',
            'advanced': '#ff5c7c'
        }
        labels = dict(Prompt.DIFFICULTY_CHOICES)
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 8px; border-radius: 3px; font-size: 10px;">{}</span>',
            colors.get(obj.difficulty, '#999'), labels.get(obj.difficulty, obj.difficulty)
        )
    difficulty_badge.short_description = "سطح"

    def make_featured(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} پرامت به عنوان ویژه علامت‌گذاری شد.')
    make_featured.short_description = "علامت‌گذاری به عنوان ویژه"

    def make_unfeatured(self, request, queryset):
        updated = queryset.update(is_featured=False)
        self.message_user(request, f'{updated} پرامت از حالت ویژه خارج شد.')
    make_unfeatured.short_description = "حذف از حالت ویژه"

    def publish_selected(self, request, queryset):
        from django.utils import timezone
        updated = queryset.update(is_published=True, published_at=timezone.now())
        self.message_user(request, f'{updated} پرامت منتشر شد.')
    publish_selected.short_description = "انتشار انتخاب شده‌ها"

    def unpublish_selected(self, request, queryset):
        updated = queryset.update(is_published=False)
        self.message_user(request, f'{updated} پرامت از حالت انتشار خارج شد.')
    unpublish_selected.short_description = "لغو انتشار"

    def duplicate_prompts(self, request, queryset):
        count = 0
        for prompt in queryset:
            prompt.pk = None
            prompt.title = f"{prompt.title} (کپی)"
            prompt.slug = f"{prompt.slug}-copy-{count}"
            prompt.views_count = 0
            prompt.likes_count = 0
            prompt.copies_count = 0
            prompt.is_published = False
            prompt.save()
            count += 1
        self.message_user(request, f'{count} پرامت کپی شد.')
    duplicate_prompts.short_description = "کپی کردن پرامت‌ها"


@admin.register(PromptCollection)
class PromptCollectionAdmin(admin.ModelAdmin):
    list_display = ['name', 'prompt_count', 'is_featured', 'created_at']
    list_filter = ['is_featured', 'created_at']
    search_fields = ['name', 'description']
    filter_horizontal = ['prompts']
    prepopulated_fields = {'slug': ('name',)}

    def prompt_count(self, obj):
        return obj.prompts.count()
    prompt_count.short_description = "تعداد پرامت"


# سفارشی‌سازی ادمین سایت
admin.site.site_header = "Poogo - پنل مدیریت پیشرفته"
admin.site.site_title = "Poogo Admin"
admin.site.index_title = "داشبورد مدیریت"
