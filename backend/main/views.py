import json
import os
import logging
from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from PIL import Image

# ВАЖНО: Импортируем модель из вашего приложения auth_app
# Так как main и auth_app - разные папки, импорт выглядит так:
from auth_app.models import CatPart

# Импортируем сервис отправки писем (предполагаем, что он лежит в папке main)
try:
    from .email_service import send_cat_email
except ImportError:
    # Заглушка, если файла нет
    def send_cat_email(*args, **kwargs):
        print("Ошибка: email_service.py не найден в папке main!")
        return False

logger = logging.getLogger(__name__)


# ==========================================
# 1. ГЕНЕРАТОР КАРТИНОК (Код напарника)
# ==========================================
class CatImageGenerator:
    @staticmethod
    def generate_cat_image(head_path, body_path, output_filename=None):
        try:
            head_img = Image.open(head_path).convert('RGBA')
            body_img = Image.open(body_path).convert('RGBA')

            max_size = 500
            if head_img.size[0] > max_size or head_img.size[1] > max_size:
                head_img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
            if body_img.size[0] > max_size or body_img.size[1] > max_size:
                body_img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)

            width = max(body_img.width, head_img.width)
            overlap = int(head_img.height * 0.3)
            height = body_img.height + head_img.height - overlap

            cat_image = Image.new('RGBA', (width, height), (255, 255, 255, 0))

            body_x = (width - body_img.width) // 2
            body_y = height - body_img.height
            cat_image.paste(body_img, (body_x, body_y), body_img)

            head_x = (width - head_img.width) // 2
            head_y = body_y - head_img.height + overlap
            cat_image.paste(head_img, (head_x, head_y), head_img)

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


# ==========================================
# 2. API СОХРАНЕНИЯ КОТА (Обновленное под БД)
# ==========================================
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

        # Получаем данные
        data = json.loads(request.body)

        # ВАЖНО: Теперь мы берем ID, а не индексы
        head_id = data.get('head_id')
        body_id = data.get('body_id')
        cat_name = data.get('cat_name', 'Без имени').strip()

        if not cat_name:
            return JsonResponse({'success': False, 'error': 'Имя котика не может быть пустым'})

        # Ищем детали в Вашей Базе Данных (auth_app.models.CatPart)
        try:
            head_part = CatPart.objects.get(id=head_id)
            body_part = CatPart.objects.get(id=body_id)
        except CatPart.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Ошибка: Деталь не найдена в базе данных'})
        except ValueError:
            return JsonResponse({'success': False, 'error': 'Ошибка: Некорректный ID детали'})

        # Получаем пути к файлам
        try:
            head_path = head_part.image.path
            body_path = body_part.image.path
        except ValueError:
            return JsonResponse({'success': False, 'error': 'У детали нет файла картинки'})

        if not os.path.exists(head_path) or not os.path.exists(body_path):
            return JsonResponse({'success': False, 'error': 'Файл картинки не найден на сервере'})

        # Генерируем
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_filename = f'cat_{request.user.id}_{timestamp}.png'

        cat_image_path, _ = CatImageGenerator.generate_cat_image(
            head_path,
            body_path,
            output_filename
        )

        if not cat_image_path:
            return JsonResponse({'success': False, 'error': 'Не удалось создать изображение'})

        # Данные для письма
        cat_data = {
            'cat_name': cat_name,
            'head_name': head_part.name,
            'body_name': body_part.name,
            'created_at': datetime.now().strftime('%d.%m.%Y %H:%M')
        }

        # Отправляем
        email_sent = send_cat_email(request.user, cat_data, cat_image_path)

        if email_sent:
            return JsonResponse({
                'success': True,
                'email_sent': True,
                'message': f'Котик "{cat_name}" отправлен на {request.user.email}!',
            })
        else:
            return JsonResponse({
                'success': True,
                'email_sent': False,
                'warning': 'Ошибка отправки почты',
                'message': f'Котик "{cat_name}" сохранен (письмо не ушло)',
            })

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'JSON Error'}, status=400)
    except Exception as e:
        logger.error(f"Ошибка сохранения: {str(e)}", exc_info=True)
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


# ==========================================
# 3. СТРАНИЦЫ MAIN (Главная и прочее)
# ==========================================

def home_page(request):
    """Главная страница"""
    return render(request, 'index.html')


@login_required
def orders_page(request):
    """Страница заказов (если она нужна напарнику)"""
    return render(request, 'orders.html')

# Заметьте: catalog_page, cart_page, builder_page УДАЛЕНЫ,
# так как они теперь обслуживаются в auth_app/views.py