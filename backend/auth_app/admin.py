from django.contrib import admin
from .models import CatPart, Profile, CartItem, Cat

# Регистрируем модели, чтобы их было видно в админке
@admin.register(CatPart)
class CatPartAdmin(admin.ModelAdmin):
    list_display = ('name', 'part_type', 'price', 'is_default')
    list_filter = ('part_type', 'is_default')
    search_fields = ('name',)

# Можно зарегистрировать и остальные, чтобы проверять корзину
admin.site.register(Profile)
admin.site.register(CartItem)
admin.site.register(Cat)