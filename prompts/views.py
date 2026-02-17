from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.cache import cache_page
from .models import Prompt, Category, SubCategory, Tag, PromptCollection


def home(request):
    """صفحه اصلی با پرامت‌های ویژه و جدید"""
    featured_prompts = Prompt.objects.filter(is_published=True, is_featured=True).select_related('category').prefetch_related('tags')[:6]
    recent_prompts = Prompt.objects.filter(is_published=True).select_related('category').prefetch_related('tags')[:12]
    categories = Category.objects.filter(is_active=True).annotate(
        prompt_count=Count('prompts', filter=Q(prompts__is_published=True))
    )[:8]
    
    context = {
        'featured_prompts': featured_prompts,
        'recent_prompts': recent_prompts,
        'categories': categories,
    }
    return render(request, 'prompts/home.html', context)


def prompt_list(request):
    """لیست تمام پرامت‌ها با فیلتر و جستجو"""
    prompts = Prompt.objects.filter(is_published=True).select_related('category', 'subcategory').prefetch_related('tags')
    
    # فیلتر دسته‌بندی
    category_slug = request.GET.get('category')
    if category_slug:
        prompts = prompts.filter(category__slug=category_slug)
    
    # فیلتر زیردسته
    subcategory_slug = request.GET.get('subcategory')
    if subcategory_slug:
        prompts = prompts.filter(subcategory__slug=subcategory_slug)
    
    # فیلتر تگ
    tag_slug = request.GET.get('tag')
    if tag_slug:
        prompts = prompts.filter(tags__slug=tag_slug)
    
    # فیلتر سطح دشواری
    difficulty = request.GET.get('difficulty')
    if difficulty:
        prompts = prompts.filter(difficulty=difficulty)
    
    # فیلتر زبان
    language = request.GET.get('language')
    if language:
        prompts = prompts.filter(language=language)
    
    # جستجو
    search_query = request.GET.get('q')
    if search_query:
        prompts = prompts.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(tags__name__icontains=search_query)
        ).distinct()
    
    # مرتب‌سازی
    sort_by = request.GET.get('sort', 'newest')
    if sort_by == 'popular':
        prompts = prompts.order_by('-views_count', '-likes_count')
    elif sort_by == 'liked':
        prompts = prompts.order_by('-likes_count')
    elif sort_by == 'copied':
        prompts = prompts.order_by('-copies_count')
    else:
        prompts = prompts.order_by('-created_at')
    
    # صفحه‌بندی
    paginator = Paginator(prompts, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # داده‌های فیلتر
    categories = Category.objects.filter(is_active=True).annotate(
        prompt_count=Count('prompts', filter=Q(prompts__is_published=True))
    )
    
    tags = Tag.objects.annotate(
        prompt_count=Count('prompts', filter=Q(prompts__is_published=True))
    ).order_by('-prompt_count')[:20]
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'tags': tags,
        'current_category': category_slug,
        'current_tag': tag_slug,
        'current_difficulty': difficulty,
        'current_language': language,
        'search_query': search_query,
        'sort_by': sort_by,
    }
    return render(request, 'prompts/prompt_list.html', context)


def prompt_detail(request, slug):
    """صفحه جزئیات پرامت"""
    prompt = get_object_or_404(Prompt, slug=slug, is_published=True)
    
    # افزایش تعداد بازدید
    prompt.increment_views()
    
    # پرامت‌های مرتبط
    related_prompts = Prompt.objects.filter(
        category=prompt.category,
        is_published=True
    ).exclude(id=prompt.id)[:6]
    
    context = {
        'prompt': prompt,
        'related_prompts': related_prompts,
    }
    return render(request, 'prompts/prompt_detail.html', context)


@require_POST
def copy_prompt(request, slug):
    """افزایش تعداد کپی پرامت (AJAX)"""
    prompt = get_object_or_404(Prompt, slug=slug, is_published=True)
    prompt.increment_copies()
    return JsonResponse({'success': True, 'copies_count': prompt.copies_count})


def category_detail(request, slug):
    """صفحه دسته‌بندی با زیردسته‌ها"""
    category = get_object_or_404(Category, slug=slug, is_active=True)
    subcategories = category.subcategories.all()
    
    prompts = Prompt.objects.filter(category=category, is_published=True).select_related('category', 'subcategory').prefetch_related('tags').order_by('-created_at')
    
    # فیلتر زیردسته اگر انتخاب شده باشد
    subcategory_slug = request.GET.get('subcategory')
    if subcategory_slug:
        prompts = prompts.filter(subcategory__slug=subcategory_slug)
    
    paginator = Paginator(prompts, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'subcategories': subcategories,
        'page_obj': page_obj,
    }
    return render(request, 'prompts/category_detail.html', context)


def collection_detail(request, slug):
    """صفحه مجموعه پرامت‌ها"""
    collection = get_object_or_404(PromptCollection, slug=slug)
    prompts = collection.prompts.filter(is_published=True).select_related('category', 'subcategory').prefetch_related('tags')
    
    context = {
        'collection': collection,
        'prompts': prompts,
    }
    return render(request, 'prompts/collection_detail.html', context)


def education_section(request):
    """بخش آموزش برنامه‌نویسی با دسته‌بندی پیشرفته"""
    # دسته‌بندی‌های مرتبط با آموزش
    education_categories = Category.objects.filter(
        is_active=True,
        slug__in=['code', 'education', 'programming']
    )
    
    # پرامت‌های آموزشی بر اساس سطح
    beginner_prompts = Prompt.objects.filter(
        is_published=True,
        difficulty='beginner',
        category__in=education_categories
    ).select_related('category', 'subcategory').prefetch_related('tags')[:10]
    
    intermediate_prompts = Prompt.objects.filter(
        is_published=True,
        difficulty='intermediate',
        category__in=education_categories
    ).select_related('category', 'subcategory').prefetch_related('tags')[:10]
    
    advanced_prompts = Prompt.objects.filter(
        is_published=True,
        difficulty='advanced',
        category__in=education_categories
    ).select_related('category', 'subcategory').prefetch_related('tags')[:10]
    
    # مجموعه‌های آموزشی
    education_collections = PromptCollection.objects.filter(is_featured=True)[:6]
    
    context = {
        'education_categories': education_categories,
        'beginner_prompts': beginner_prompts,
        'intermediate_prompts': intermediate_prompts,
        'advanced_prompts': advanced_prompts,
        'education_collections': education_collections,
    }
    return render(request, 'prompts/education.html', context)
