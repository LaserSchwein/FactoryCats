from django.urls import path, include
from . import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home_page, name='home'),
    path('catalog/', views.catalog_page, name='catalog'),
    path('cart/', views.cart_page, name='cart'),
    path('checkout/', views.checkout_page, name='checkout'),
    path('profile/', views.profile_page, name='profile'),
    path('orders/', views.orders_page, name='orders'),
    path('auth/', include('auth_app.urls')),
    path('admin/', admin.site.urls),
    path('builder/', views.builder_page, name='builder'),
    path('logout/', views.logout_view, name='logout'),
    path('', include('auth_app.urls')),  # Путь к auth_app
    path('api/save-cat/', views.save_and_send_cat, name='save_and_send_cat'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
