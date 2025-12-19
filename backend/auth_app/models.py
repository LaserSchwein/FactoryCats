from django.db import models
from django.contrib.auth.models import User


class CatPart(models.Model):
    """Части котов (головы и туловища)"""

    PART_TYPES = [
        ('head', 'Голова'),
        ('body', 'Туловище'),
    ]

    name = models.CharField(max_length=100, verbose_name='Название')
    part_type = models.CharField(max_length=10, choices=PART_TYPES, verbose_name='Тип')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    image = models.ImageField(upload_to='cat_parts/', verbose_name='Изображение')
    description = models.TextField(blank=True, verbose_name='Описание')
    is_default = models.BooleanField(default=False, verbose_name='Доступно по умолчанию')

    class Meta:
        verbose_name = 'Часть кота'
        verbose_name_plural = 'Части котов'

    def __str__(self):
        return f"{self.get_part_type_display()}: {self.name}"


class Profile(models.Model):
    """Профиль пользователя"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    first_name = models.CharField(max_length=100, blank=True, verbose_name='Имя')
    last_name = models.CharField(max_length=100, blank=True, verbose_name='Фамилия')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Баланс')

    # Купленные части (Many-to-Many)
    owned_parts = models.ManyToManyField(CatPart, blank=True, verbose_name='Купленные части')

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return f"Профиль {self.user.username}"


class CartItem(models.Model):
    """Корзина покупок"""

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='cart_items', verbose_name='Профиль')
    part = models.ForeignKey(CatPart, on_delete=models.CASCADE, verbose_name='Часть')
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='Добавлено')

    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'

    def __str__(self):
        return f"{self.part.name} в корзине {self.profile.user.username}"


class Cat(models.Model):
    """Собранный кот"""

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='cats', verbose_name='Владелец')
    name = models.CharField(max_length=100, verbose_name='Имя кота')
    head = models.ForeignKey(CatPart, on_delete=models.CASCADE, related_name='cats_as_head', verbose_name='Голова')
    body = models.ForeignKey(CatPart, on_delete=models.CASCADE, related_name='cats_as_body', verbose_name='Туловище')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    sent_to_email = models.BooleanField(default=False, verbose_name='Отправлен на почту')

    class Meta:
        verbose_name = 'Кот'
        verbose_name_plural = 'Коты'

    def __str__(self):
        return f"Кот {self.name} ({self.profile.user.username})"
