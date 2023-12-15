"""
В этом задании вам предстоит работать с моделью ноутбука. У него есть бренд (один из нескольких вариантов),
год выпуска, количество оперативной памяти, объём жесткого диска, цена, количество этих ноутбуков на складе
и дата добавления.

Ваша задача:
- создать соответствующую модель (в models.py)
- создать и применить миграцию по созданию модели (миграцию нужно добавить в пул-реквест)
- заполнить вашу локальную базу несколькими ноутбуками для облегчения тестирования
  (я бы советовал использовать для этого shell)
- реализовать у модели метод to_json, который будет преобразовывать объект ноутбука в json-сериализуемый словарь
- по очереди реализовать каждую из вьюх в этом файле, проверяя правильность их работу в браузере
"""
import json

from django.db.models import QuerySet
from django.http import (HttpRequest, HttpResponse, HttpResponseForbidden,
                         HttpResponseNotFound)

from challenges.models import Laptop


def get_dict_for_queryset(queryset: QuerySet):
    data = [item.to_json() for item in queryset]
    return data


def laptop_details_view(request: HttpRequest, laptop_id: int) -> HttpResponse:
    """
    В этой вьюхе вам нужно вернуть json-описание ноутбука по его id.
    Если такого id нет, вернуть 404.
    """
    try:
        laptop = Laptop.objects.get(pk=laptop_id)
    except Laptop.DoesNotExist:
        return HttpResponseNotFound("This laptop doesn't exist")
    return HttpResponse(json.dumps(laptop.to_json()))


def laptop_in_stock_list_view(request: HttpRequest) -> HttpResponse:
    """
    В этой вьюхе вам нужно вернуть json-описание всех ноутбуков, которых на складе больше нуля.
    Отсортируйте ноутбуки по дате добавления, сначала самый новый.
    """
    laptops = Laptop.objects.filter(quantity__gt=0).order_by('-created_at').all()
    return HttpResponse(json.dumps(get_dict_for_queryset(laptops)))


def laptop_filter_view(request: HttpRequest) -> HttpResponse:
    """
    В этой вьюхе вам нужно вернуть список ноутбуков с указанным брендом и указанной минимальной ценой.
    Бренд и цену возьмите из get-параметров с названиями brand и min_price.
    Если бренд не входит в список доступных у вас на сайте или если цена отрицательная, верните 403.
    Отсортируйте ноутбуки по цене, сначала самый дешевый.
    """
    brand = request.GET.get('brand')
    min_price = request.GET.get('min_price')
    if not all([brand, min_price]):
        return HttpResponseForbidden('Some reqired parameters are missing!')
    laptops = Laptop.objects.filter(brand=brand, price__gte=min_price).all()
    if not laptops:
        return HttpResponseForbidden('No laptops with this params!')
    return HttpResponse(json.dumps(get_dict_for_queryset(laptops)))


def last_laptop_details_view(request: HttpRequest) -> HttpResponse:
    """
    В этой вьюхе вам нужно вернуть json-описание последнего созданного ноутбука.
    Если ноутбуков нет вообще, вернуть 404.
    """
    laptop = Laptop.objects.order_by('-created_at').first()
    if not laptop:
        return HttpResponseNotFound('No laptops!')

    return HttpResponse(json.dumps(laptop.to_json()))
