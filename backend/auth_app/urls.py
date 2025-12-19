from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Авторизация
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_page, name='profile'),

    # Ваш функционал (Каталог, Корзина, Конструктор)
    path('catalog/', views.catalog, name='catalog'),
    path('builder/', views.builder, name='builder'),

    # Корзина и оформление
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
]

# Эту часть можно убрать отсюда, так как она уже есть в main/urls.py,
# но если оставите - ошибки не будет.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)