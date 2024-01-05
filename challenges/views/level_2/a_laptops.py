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
from django.http import HttpRequest, JsonResponse
from django.core.exceptions import ValidationError

from challenges.models import Laptop
from typing import Any


def get_dict_for_queryset(queryset: QuerySet) -> list[dict[str, Any]]:
    data = [item.to_json() for item in queryset]

    return data


def validate_price_and_brand(params: dict[str, Any]) -> None:
    brand = params.get('brand')
    min_price = params.get('min_price')

    if not brand:
        raise ValidationError('parameter "brand" is missing')
    if not min_price:
        raise ValidationError('parameter "min_price" is missing')
    
    try:
        price = int(min_price)
    except ValueError:
        raise ValidationError('parametr "min_price" is not number')
    if price < 0:
        raise ValidationError('parametr "min_price" should be > 0')


def laptop_details_view(request: HttpRequest, laptop_id: int) -> JsonResponse:
    """
    В этой вьюхе вам нужно вернуть json-описание ноутбука по его id.
    Если такого id нет, вернуть 404.
    """
    try:
        laptop = Laptop.objects.get(pk=laptop_id)
    except Laptop.DoesNotExist:
        return JsonResponse({"error": {'code': 'not_found', 'message': 'laptop not found'}}, status=404)
    return JsonResponse(laptop.to_json())


def laptop_in_stock_list_view(request: HttpRequest) -> JsonResponse:
    """
    В этой вьюхе вам нужно вернуть json-описание всех ноутбуков, которых на складе больше нуля.
    Отсортируйте ноутбуки по дате добавления, сначала самый новый.
    """
    laptops = Laptop.objects.filter(quantity__gt=0).order_by('-created_at')
    return JsonResponse(get_dict_for_queryset(laptops), safe=False)


def laptop_filter_view(request: HttpRequest) -> JsonResponse:
    """
    В этой вьюхе вам нужно вернуть список ноутбуков с указанным брендом и указанной минимальной ценой.
    Бренд и цену возьмите из get-параметров с названиями brand и min_price.
    Если бренд не входит в список доступных у вас на сайте или если цена отрицательная, верните 403.
    Отсортируйте ноутбуки по цене, сначала самый дешевый.
    """
    params = request.GET
    try:
        validate_price_and_brand(params)
    except ValidationError as e:
        return JsonResponse({"error": {'code': 'validation_error', 'message': list(e)[0]}}, status=403)
    
    brand = params.get('brand')
    min_price = params.get('min_price')
    laptops = Laptop.objects.filter(brand=brand)

    if not laptops:
        return JsonResponse({"error": {'code': 'validation_error', 'message': 'there is no this brand in store'}}, status=403)
    laptops = laptops.filter(price__gte=min_price).order_by('price')

    if not laptops:
        return JsonResponse({"error": {'code': 'not_found', 'message': 'laptops not found'}}, status=404)
    return JsonResponse(get_dict_for_queryset(laptops), safe=False)


def last_laptop_details_view(request: HttpRequest) -> JsonResponse:
    """
    В этой вьюхе вам нужно вернуть json-описание последнего созданного ноутбука.
    Если ноутбуков нет вообще, вернуть 404.
    """
    laptop = Laptop.objects.order_by('-created_at').first()
    if not laptop:
        return JsonResponse({"error": {'code': 'not_found', 'message': 'laptop not found'}}, status=404)
    return JsonResponse(laptop.to_json())
