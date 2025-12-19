from PIL import Image
import os
from django.conf import settings
from datetime import datetime


class CatImageGenerator:
    @staticmethod
    def generate_cat_image(head_path, body_path, output_filename=None):
        """
        Генерирует изображение котика, совмещая голову и тело

        Args:
            head_path: путь к изображению головы
            body_path: путь к изображению тела
            output_filename: имя файла для сохранения (если None - генерируется автоматически)

        Returns:
            tuple: (путь к сохраненному файлу, имя файла)
        """
        try:
            # Открываем изображения
            head_img = Image.open(head_path).convert('RGBA')
            body_img = Image.open(body_path).convert('RGBA')

            # Проверяем размеры и масштабируем при необходимости
            if head_img.size[0] > 500 or head_img.size[1] > 500:
                head_img.thumbnail((500, 500), Image.Resampling.LANCZOS)

            if body_img.size[0] > 500 or body_img.size[1] > 500:
                body_img.thumbnail((500, 500), Image.Resampling.LANCZOS)

            # Создаем новое изображение (размер как у тела или больше)
            width = max(body_img.width, head_img.width)
            height = body_img.height + head_img.height - 50  # Наложение

            cat_image = Image.new('RGBA', (width, height), (255, 255, 255, 0))

            # Размещаем тело
            body_x = (width - body_img.width) // 2
            body_y = height - body_img.height
            cat_image.paste(body_img, (body_x, body_y), body_img)

            # Размещаем голову поверх тела
            head_x = (width - head_img.width) // 2
            head_y = body_y - head_img.height + 50  # Наложение
            cat_image.paste(head_img, (head_x, head_y), head_img)

            # Создаем папку для сохранения, если её нет
            save_dir = os.path.join(settings.MEDIA_ROOT, 'generated_cats')
            os.makedirs(save_dir, exist_ok=True)

            # Генерируем имя файла
            if output_filename is None:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                output_filename = f'cat_{timestamp}.png'

            output_path = os.path.join(save_dir, output_filename)

            # Сохраняем изображение
            cat_image.save(output_path, 'PNG')

            # Также создаем JPEG версию для совместимости
            jpg_path = output_path.replace('.png', '.jpg')
            cat_image.convert('RGB').save(jpg_path, 'JPEG', quality=95)

            return output_path, output_filename

        except Exception as e:
            print(f"Ошибка генерации изображения: {e}")
            return None, None

    @staticmethod
    def get_static_image_path(filename):
        """Получает полный путь к статическому изображению"""
        return os.path.join(settings.STATICFILES_DIRS[0], 'images', filename)