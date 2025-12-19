from django.urls import path, include
from . import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Оставляем главную, если она работает через main.views
    path('', views.home_page, name='home'),

    # Оставляем админку
    path('admin/', admin.site.urls),

    # API, если его делали напарники и оно нужно
    path('api/save-cat/', views.save_and_send_cat, name='save_and_send_cat'),

    # ВАЖНО: Все остальные пути (каталог, корзина, логин, профиль, конструктор)
    # мы отправляем искать в auth_app.urls
    path('', include('auth_app.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)