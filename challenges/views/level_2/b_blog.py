"""
В этом задании вам предстоит работать с моделью поста в блоге. У него есть название, текст, имя автора, статус
(опубликован/не опубликован/забанен), дата создания, дата публикации, категория (одна из нескольких вариантов).

Ваша задача:
- создать соответствующую модель (в models.py)
- создать и применить миграцию по созданию модели (миграцию нужно добавить в пул-реквест)
- заполнить вашу локальную базу несколькими ноутбуками для облегчения тестирования
- реализовать у модели метод to_json, который будет преобразовывать объект книги в json-сериализуемый словарь
- по очереди реализовать каждую из вьюх в этом файле, проверяя правильность их работу в браузере
"""
import json
from datetime import datetime, timedelta

from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest

from challenges.models import Blog


def get_dict_for_queryset(queryset: QuerySet):
    data = [item.to_json() for item in queryset]
    return data


def last_posts_list_view(request: HttpRequest) -> HttpResponse:
    """
    В этой вьюхе вам нужно вернуть 3 последних опубликованных поста.
    """
    return HttpResponse(json.dumps(get_dict_for_queryset(Blog.objects.all()[:3])))


def posts_search_view(request: HttpRequest) -> HttpResponse:
    """
    В этой вьюхе вам нужно вернуть все посты, которые подходят под поисковый запрос.
    Сам запрос возьмите из get-параметра query.
    Подходящесть поста можете определять по вхождению запроса в название или текст поста, например.
    """
    title = request.GET.get('title')
    text = request.GET.get('text')
    if not any([title, text]):
        return HttpResponseBadRequest('Required params are missing!')
    all_posts = Blog.objects.all()

    if title and text:
        posts = all_posts.filter(title=title, text__icontains=text)
    
    if title:
        posts = all_posts.filter(title=title)
    
    if text:
        posts = all_posts.filter(text__icontains=text)

    return HttpResponse(json.dumps(get_dict_for_queryset(posts)))


def untagged_posts_list_view(request: HttpRequest) -> HttpResponse:
    """
    В этой вьюхе вам нужно вернуть все посты без категории, отсортируйте их по автору и дате создания.
    """
    posts = Blog.objects.filter(category__isnull=True).order_by('author', '-created_at').all()
    return HttpResponse(json.dumps(get_dict_for_queryset(posts)))


def categories_posts_list_view(request: HttpRequest) -> HttpResponse:
    """
    В этой вьюхе вам нужно вернуть все посты все посты, категория которых принадлежит одной из указанных.
    Возьмите get-параметр categories, в нём разделённый запятой список выбранных категорий.
    """
    categories_raw = request.GET.get('categories')
    if not categories_raw:
        return HttpResponseBadRequest('Required params are missing!')
    categories = categories_raw.split(',')
    categories = [category.strip() for category in categories]
    posts = Blog.objects.filter(category__in=categories)

    return HttpResponse(json.dumps(get_dict_for_queryset(posts)))


def last_days_posts_list_view(request: HttpRequest) -> HttpResponse:
    """
    В этой вьюхе вам нужно вернуть посты, опубликованные за последние last_days дней.
    Значение last_days возьмите из соответствующего get-параметра.
    """
    last_days = request.GET.get('last_days')
    
    if not last_days:
        return HttpResponseBadRequest('Missing parametr "last_days"')
    try:
        last_days = int(last_days)
    except TypeError:
        return HttpResponseBadRequest('Parametr "last_days" should be integer')
    datetime_now = datetime.now() - timedelta(days=last_days)
    posts = Blog.objects.filter(published_at__gte=datetime_now).all()

    return HttpResponse(json.dumps(get_dict_for_queryset(posts)))
