from django.urls import path, re_path
from . import views

# Pattern برای slug های فارسی و انگلیسی - پذیرش تمام کاراکترهای Unicode
# شامل: خط تیره، underscore، اعداد، حروف انگلیسی و فارسی/عربی
slug_pattern = r'[-\w\u0600-\u06FF]+'

urlpatterns = [
    path('', views.home, name='home'),
    path('prompts/', views.prompt_list, name='prompt_list'),
    re_path(r'^prompt/(?P<slug>' + slug_pattern + r')/$', views.prompt_detail, name='prompt_detail'),
    re_path(r'^prompt/(?P<slug>' + slug_pattern + r')/copy/$', views.copy_prompt, name='copy_prompt'),
    re_path(r'^category/(?P<slug>' + slug_pattern + r')/$', views.category_detail, name='category_detail'),
    re_path(r'^collection/(?P<slug>' + slug_pattern + r')/$', views.collection_detail, name='collection_detail'),
    path('education/', views.education_section, name='education'),
]
