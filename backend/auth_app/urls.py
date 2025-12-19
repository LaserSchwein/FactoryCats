from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_page, name='profile'),
    path('catalog/', views.catalog, name='catalog'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('builder/', views.builder, name='builder'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)