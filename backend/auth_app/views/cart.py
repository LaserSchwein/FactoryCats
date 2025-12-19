from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import Profile, CartItem


@login_required
def cart_view(request):
    """Страница корзины"""
    profile = Profile.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(profile=profile)

    # Считаем сумму
    total_price = sum(item.part.price for item in cart_items)

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })


@login_required
def remove_from_cart(request, item_id):
    """Удаление товара из корзины (крестик)"""
    cart_item = get_object_or_404(CartItem, id=item_id, profile__user=request.user)
    cart_item.delete()
    return redirect('cart')


@login_required
def checkout(request):
    """Страница оформления заказа и оплата"""
    profile = Profile.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(profile=profile)
    total_price = sum(item.part.price for item in cart_items)

    # Если корзина пуста, выкидываем обратно в каталог
    if not cart_items:
        return redirect('catalog')

    # Если нажали кнопку "Подтвердить" (POST запрос)
    if request.method == 'POST':
        if profile.balance >= total_price:
            # 1. Списываем деньги
            profile.balance -= total_price

            # 2. Добавляем товары в купленные
            for item in cart_items:
                profile.owned_parts.add(item.part)

            # 3. Очищаем корзину
            cart_items.delete()

            # 4. Сохраняем профиль
            profile.save()

            messages.success(request, "Поздравляем! Покупка успешна.")
            return redirect('profile')  # Или куда вы хотите после покупки
        else:
            messages.error(request, "Ошибка: Недостаточно средств на балансе!")
            # Не перенаправляем, чтобы пользователь увидел ошибку на этой же странице

    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'profile': profile
    })