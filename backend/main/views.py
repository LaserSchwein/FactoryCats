from django.contrib.auth.decorators import login_required
from django.shortcuts import render

def home_page(request):
    return render(request, 'index.html')

def catalog_page(request):
    return render(request, 'catalog.html')

def cart_page(request):
    return render(request, 'cart/cart.html')

def checkout_page(request):
    return render(request, 'cart/checkout.html')

def profile_page(request):
    return render(request, 'profile.html')

def orders_page(request):
    return render(request, 'orders.html')

@login_required
def builder_page(request):
    return render(request, 'builder.html')