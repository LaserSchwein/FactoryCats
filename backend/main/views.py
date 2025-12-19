import json
import os
import logging
from datetime import datetime

from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from PIL import Image

logger = logging.getLogger(__name__)

# Импортируем нашу работающую email функцию
from .email_service import send_cat_email


class CatImageGenerator:
    @staticmethod
    def generate_cat_image(head_path, body_path, output_filename=None):
        try:
            # Открываем изображения
            head_img = Image.open(head_path).convert('RGBA')
            body_img = Image.open(body_path).convert('RGBA')

            # Масштабируем
            max_size = 500
            if head_img.size[0] > max_size or head_img.size[1] > max_size:
                head_img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)

            if body_img.size[0] > max_size or body_img.size[1] > max_size:
                body_img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)

            # Создаем изображение котика
            width = max(body_img.width, head_img.width)
            overlap = int(head_img.height * 0.3)
            height = body_img.height + head_img.height - overlap

            cat_image = Image.new('RGBA', (width, height), (255, 255, 255, 0))

            # Размещаем тело
            body_x = (width - body_img.width) // 2
            body_y = height - body_img.height
            cat_image.paste(body_img, (body_x, body_y), body_img)

            # Размещаем голову
            head_x = (width - head_img.width) // 2
            head_y = body_y - head_img.height + overlap
            cat_image.paste(head_img, (head_x, head_y), head_img)

            # Сохраняем
            save_dir = os.path.join('media', 'generated_cats')
            os.makedirs(save_dir, exist_ok=True)

            if output_filename is None:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                output_filename = f'cat_{timestamp}.png'

            output_path = os.path.join(save_dir, output_filename)
            cat_image.save(output_path, 'PNG')

            logger.info(f"Изображение сохранено: {output_path}")
            return output_path, output_filename

        except Exception as e:
            logger.error(f"Ошибка генерации: {str(e)}")
            return None, None

    @staticmethod
    def get_static_image_path(filename):
        try:
            return os.path.join('static', 'images', filename)
        except:
            return os.path.join('static/images', filename)


@csrf_exempt
@require_POST
@login_required
def save_and_send_cat(request):
    try:
        # Проверка email
        if not request.user.email:
            return JsonResponse({
                'success': False,
                'error': 'Укажите email в профиле'
            }, status=400)

        # Парсим данные
        data = json.loads(request.body)
        logger.info(f"Получены данные: {data}")

        # Валидация
        required_fields = ['head_index', 'body_index', 'cat_name']
        for field in required_fields:
            if field not in data:
                return JsonResponse({
                    'success': False,
                    'error': f'Отсутствует поле: {field}'
                }, status=400)

        # Проверяем индексы
        try:
            head_index = int(data['head_index'])
            body_index = int(data['body_index'])

            if head_index < 0 or head_index > 6:
                raise ValueError("Неверный индекс головы")
            if body_index < 0 or body_index > 5:
                raise ValueError("Неверный индекс тела")
        except ValueError as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })

        # Проверяем имя
        cat_name = data['cat_name'].strip()
        if not cat_name:
            return JsonResponse({
                'success': False,
                'error': 'Имя котика не может быть пустым'
            })

        # Определяем файлы
        head_files = ['head-1.png', 'head-2.png', 'head-3.png', 'head-4.png',
                      'head-5.png', 'head-6.png', 'head-7.png']
        body_files = ['body-1.png', 'body-2.png', 'body-3.png',
                      'body-4.png', 'body-5.png', 'body-6.png']

        head_names = ["Стандартная голова", "Радужная голова", "Огненная голова",
                      "Тигриная голова", "Голова Робин Гуда", "Голова Дриады", "Арктическая голова"]
        body_names = ["Стандартное тело", "Тело 'Дуэт'", "Ночное тело",
                      "Снежное тело", "Пухлое тело", "Радужное тело"]

        # Получаем пути
        head_filename = head_files[head_index]
        body_filename = body_files[body_index]

        head_path = CatImageGenerator.get_static_image_path(head_filename)
        body_path = CatImageGenerator.get_static_image_path(body_filename)

        logger.info(f"Head path: {head_path}, exists: {os.path.exists(head_path)}")
        logger.info(f"Body path: {body_path}, exists: {os.path.exists(body_path)}")

        # Проверяем файлы
        if not os.path.exists(head_path):
            return JsonResponse({
                'success': False,
                'error': f'Файл головы не найден: {head_path}'
            })

        if not os.path.exists(body_path):
            return JsonResponse({
                'success': False,
                'error': f'Файл тела не найден: {body_path}'
            })

        # Генерируем изображение
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_filename = f'cat_{request.user.id}_{timestamp}.png'

        cat_image_path, _ = CatImageGenerator.generate_cat_image(
            head_path,
            body_path,
            output_filename
        )

        if not cat_image_path:
            return JsonResponse({
                'success': False,
                'error': 'Не удалось создать изображение'
            })

        logger.info(f"Изображение создано: {cat_image_path}")

        # Подготавливаем данные для письма
        cat_data = {
            'cat_name': cat_name,
            'head_name': head_names[head_index],
            'body_name': body_names[body_index],
            'created_at': datetime.now().strftime('%d.%m.%Y %H:%M')
        }

        # Отправляем письмо
        logger.info(f"Отправляем письмо на {request.user.email}")
        email_sent = send_cat_email(request.user, cat_data, cat_image_path)

        # Возвращаем результат
        if email_sent:
            return JsonResponse({
                'success': True,
                'email_sent': True,
                'message': f'Котик "{cat_name}" отправлен на {request.user.email}!',
                'cat_name': cat_name,
                'email': request.user.email
            })
        else:
            return JsonResponse({
                'success': True,
                'email_sent': False,
                'warning': 'Котик сохранен, но не отправлен',
                'message': f'Котик "{cat_name}" сохранен',
                'cat_name': cat_name
            })

    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Неверный формат JSON'
        }, status=400)
    except Exception as e:
        logger.error(f"Ошибка в save_and_send_cat: {str(e)}", exc_info=True)
        return JsonResponse({
            'success': False,
            'error': f'Внутренняя ошибка: {str(e)}'
        }, status=500)

# Простые views
def home_page(request):
    return render(request, 'index.html')


def catalog_page(request):
    return render(request, 'catalog.html')


def cart_page(request):
    return render(request, 'cart/cart.html')


def checkout_page(request):
    return render(request, 'cart/checkout.html')


@login_required
def profile_page(request):
    return render(request, 'profile.html')


@login_required
def orders_page(request):
    return render(request, 'orders.html')


@login_required
def builder_page(request):
    return render(request, 'builder.html')

def logout_view(request):
    logout(request)
    return redirect('home')