# api/views/profile.py

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json
from ..models import Profile


# ==================== ДЛЯ HTML СТРАНИЦ ====================

@login_required
def profile_page(request):
    """Показать и обновить страницу профиля"""
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        # Обновляем данные пользователя
        user = request.user
        user.username = request.POST.get('username', user.username)
        user.email = request.POST.get('email', user.email)
        user.save()

        # Обновляем данные профиля
        profile.first_name = request.POST.get('first_name', profile.first_name)
        profile.last_name = request.POST.get('last_name', profile.last_name)
        profile.balance = request.POST.get('balance', profile.balance)
        profile.save()

        messages.success(request, 'Профиль успешно обновлён!')
        return redirect('profile')  # Перенаправляем обратно на профиль

    # Если это GET-запрос, просто отображаем профиль
    return render(request, 'profile.html', {'profile': profile})


# ==================== ДЛЯ JAVASCRIPT (API) ====================

def get_profile_api(request):
    """Получить данные профиля (JSON)"""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Не авторизован'}, status=401)

    profile = request.user.profile
    owned_parts = list(profile.owned_parts.values('id', 'name', 'part_type', 'image'))

    return JsonResponse({
        'username': request.user.username,
        'email': request.user.email,
        'first_name': profile.first_name,
        'last_name': profile.last_name,
        'balance': float(profile.balance),
        'owned_parts': owned_parts,
    })


def update_profile_api(request):
    """Обновить профиль через JavaScript (JSON)"""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Не авторизован'}, status=401)

    if request.method == 'POST':
        data = json.loads(request.body)
        user = request.user
        profile = user.profile

        # Исправление: username и email в User, не в Profile!
        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)
        user.save()

        profile.first_name = data.get('first_name', profile.first_name)
        profile.last_name = data.get('last_name', profile.last_name)
        profile.save()

        return JsonResponse({'message': 'Профиль обновлён!'})

    return JsonResponse({'error': 'Нужен POST'}, status=400)