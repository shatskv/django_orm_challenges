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
from typing import Any
from django.core.exceptions import ValidationError

from django.db.models import QuerySet
from django.http import HttpRequest, JsonResponse

from challenges.models import Blog


def validate_last_days(days: str | None) -> None:
    if days is None:
        raise ValidationError('parameter "last_days" is missing')
    try:
        int(days)
    except ValueError:
        raise ValidationError('Parameter "last_days" should be integer')
    

def get_dict_for_queryset(queryset: QuerySet) -> list[dict[str, Any]]:
    data = [item.to_json() for item in queryset]
    return data


def last_posts_list_view(request: HttpRequest) -> JsonResponse:
    """
    В этой вьюхе вам нужно вернуть 3 последних опубликованных поста.
    """
    posts = Blog.objects.filter(published_at__isnull=False).order_by('-published_at')[:3]
    return JsonResponse(get_dict_for_queryset(posts), safe=False)


def posts_search_view(request: HttpRequest) -> JsonResponse:
    """
    В этой вьюхе вам нужно вернуть все посты, которые подходят под поисковый запрос.
    Сам запрос возьмите из get-параметра query.
    Подходящесть поста можете определять по вхождению запроса в название или текст поста, например.
    """
    title = request.GET.get('title')
    text = request.GET.get('text')

    if not any([title, text]):
        return JsonResponse({"error": {'code': 'validation_error', 'message': 'required parameters are missing'}}, status=400)
    
    posts = Blog.objects.all()
    if title:
        posts = posts.filter(title__icontains=title)
    if text:
        posts = posts.filter(title__icontains=text)

    return JsonResponse(get_dict_for_queryset(posts), safe=False)


def untagged_posts_list_view(request: HttpRequest) -> JsonResponse:
    """
    В этой вьюхе вам нужно вернуть все посты без категории, отсортируйте их по автору и дате создания.
    """
    posts = Blog.objects.filter(category__isnull=True).order_by('author', '-created_at')
    return JsonResponse(get_dict_for_queryset(posts), safe=False)


def categories_posts_list_view(request: HttpRequest) -> JsonResponse:
    """
    В этой вьюхе вам нужно вернуть все посты все посты, категория которых принадлежит одной из указанных.
    Возьмите get-параметр categories, в нём разделённый запятой список выбранных категорий.
    """
    categories_raw = request.GET.get('categories')
    if not categories_raw:
        return JsonResponse({"error": {'code': 'validation_error', 'message': 'parametr "categories" is missing'}}, status=400)
    categories = categories_raw.split(',')
    categories = [category.strip().capitalize() for category in categories]

    posts = Blog.objects.filter(category__in=categories)

    return JsonResponse(get_dict_for_queryset(posts), safe=False)


def last_days_posts_list_view(request: HttpRequest) -> JsonResponse:
    """
    В этой вьюхе вам нужно вернуть посты, опубликованные за последние last_days дней.
    Значение last_days возьмите из соответствующего get-параметра.
    """
    last_days = request.GET.get('last_days')

    try:
        validate_last_days(last_days)
    except ValidationError as e:
        return JsonResponse({"error": {'code': 'validation_error', 'message': list(e)[0]}}, status=400)
    
    last_days = abs(int(last_days))
    datetime_now = datetime.now() - timedelta(days=last_days)
    posts = Blog.objects.filter(published_at__gte=datetime_now)

    return JsonResponse(get_dict_for_queryset(posts), safe=False)
