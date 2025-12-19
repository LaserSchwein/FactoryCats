from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ..models import Profile


@login_required
def builder(request):
    """Конструктор котиков"""
    try:
        profile = Profile.objects.get(user=request.user)

        # Берем ТОЛЬКО купленные части из owned_parts
        owned_parts = profile.owned_parts.all()

        # Разделяем их на головы и туловища для удобства в шаблоне
        heads = owned_parts.filter(part_type='head')
        bodies = owned_parts.filter(part_type='body')

    except Profile.DoesNotExist:
        # Если профиля нет (странно, но бывает), списки будут пустыми
        heads = []
        bodies = []

    return render(request, 'builder.html', {
        'heads': heads,
        'bodies': bodies,
    })
