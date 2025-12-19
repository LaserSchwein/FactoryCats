import json
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from ..models import CatPart, Profile, CartItem


def catalog(request):
    """Отображение каталога товаров"""
    parts = CatPart.objects.all()

    # Собираем ID товаров, которые уже в корзине у пользователя,
    # чтобы сразу показать кнопку "Уже в корзине" при загрузке страницы
    cart_part_ids = []
    if request.user.is_authenticated:
        # Пытаемся получить или создать профиль (на случай если его нет)
        profile, created = Profile.objects.get_or_create(user=request.user)
        user_cart_items = CartItem.objects.filter(profile=profile)
        cart_part_ids = [item.part.id for item in user_cart_items]

    return render(request, 'catalog.html', {
        'parts': parts,
        'cart_part_ids': cart_part_ids
    })


@login_required
@require_POST
def add_to_cart(request):
    """API для добавления товара в корзину через AJAX"""
    try:
        data = json.loads(request.body)
        part_id = data.get('part_id')

        part = CatPart.objects.get(id=part_id)
        profile, created = Profile.objects.get_or_create(user=request.user)

        # Проверяем, нет ли уже этого товара в корзине
        if not CartItem.objects.filter(profile=profile, part=part).exists():
            CartItem.objects.create(profile=profile, part=part)
            return JsonResponse({'status': 'success', 'message': 'Добавлено'})
        else:
            return JsonResponse({'status': 'exists', 'message': 'Уже в корзине'})

    except CatPart.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Товар не найден'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)