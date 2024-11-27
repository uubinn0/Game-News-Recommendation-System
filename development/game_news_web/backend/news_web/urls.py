"""news_web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.http import HttpResponse
from users.views import signup, login, update_user_info
from webvue.views import vue_index
from articles.views import read_article_list, push_like, remove_like
from articles.views import get_news_RAG
urlpatterns = [
    path('api/signup/', signup),
    path('api/login/', login),
    # path('api/article/list/', read_article_list),
    path('api/article/list/<str:category>/', read_article_list, name='read_article_list_with_category'),
    path('api/article/list/like/<str:url>/', push_like, name='push_like'),
    path('api/article/list/unlike/<str:url>/', remove_like, name='remove_like'),
    path('api/user/update_info/', update_user_info, name='update_user_info'),
    # category가 없는 경우
    path('api/article/list/', read_article_list, name='read_article_list_without_category'),
    path('', vue_index, name='vue_index'),
    path('api/article/RAG/<str:url>/', get_news_RAG, name='get_news_RAG'),
    re_path(r'^(?:.*)/?$', vue_index),  # 항상 마지막에 배치
]

