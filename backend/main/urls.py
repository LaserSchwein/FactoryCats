from django.urls import path, include

from . import views  # Используйте относительный импорт

urlpatterns = [
    path('', views.home_page, name='home'),
    path('catalog/', views.catalog_page, name='catalog'),
    path('cart/', views.cart_page, name='cart'),
    path('checkout/', views.checkout_page, name='checkout'),
    path('profile/', views.profile_page, name='profile'),
    path('orders/', views.orders_page, name='orders'),
    path('builder/', views.builder_page, name='builder'),
    path('logout/', views.logout_view, name='logout'),
    path('', include('auth_app.urls')),  # Путь к auth_app

    # API endpoints
    path('api/save-cat/', views.save_and_send_cat, name='save_and_send_cat'),
]