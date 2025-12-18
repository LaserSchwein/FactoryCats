from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('catalog/', views.catalog_page, name='catalog'),
    path('builder/', views.builder_page, name='builder'),
    path('cart/', views.cart_page, name='cart'),
    path('checkout/', views.checkout_page, name='checkout'),
    #path('profile/', views.profile_page, name='profile'),
    path('orders/', views.orders_page, name='orders'),
    path('auth/', include('auth_app.urls')),
]
