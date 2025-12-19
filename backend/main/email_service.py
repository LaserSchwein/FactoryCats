import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import logging
import os
import ssl  # Нужно для защищенного соединения

logger = logging.getLogger(__name__)


def send_email_direct(to_email, subject, text_content, html_content=None, image_path=None):
    # --- НАСТРОЙКИ SMTP YANDEX ---
    smtp_server = "smtp.yandex.ru"
    port = 465  # <--- ВАЖНО: Используем 465 (SSL) вместо 587

    sender_email = "cotofabrica@yandex.ru"
    # Пароль приложения (который был у вас в коде)
    password = "dvqhcxuijzzhrsbt"

    try:
        # 1. Формируем письмо
        msg = MIMEMultipart('related')
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = to_email

        # Текст
        msg.attach(MIMEText(text_content, 'plain', 'utf-8'))

        # HTML
        if html_content:
            msg.attach(MIMEText(html_content, 'html', 'utf-8'))

        # Картинка
        if image_path:
            if os.path.exists(image_path):
                with open(image_path, 'rb') as f:
                    img_data = f.read()
                image = MIMEImage(img_data)
                image.add_header('Content-ID', '<cat_image>')
                image.add_header('Content-Disposition', 'inline', filename='cat.png')
                msg.attach(image)
            else:
                print(f"⚠️ Файл картинки не найден: {image_path}")

        # 2. Подключаемся через SSL (Это решает проблему Connection closed)
        print(f"🔄 Подключение к {smtp_server}:{port} через SSL...")

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.send_message(msg)

        print(f"✅ Письмо успешно отправлено на {to_email}")
        return True

    except smtplib.SMTPAuthenticationError:
        print("❌ Ошибка авторизации! Яндекс не принял пароль.")
        logger.error("SMTP Auth Error")
        return False
    except Exception as e:
        print(f"❌ Ошибка отправки: {e}")
        logger.error(f"SMTP Error: {e}")
        return False


def send_cat_email(user, cat_data, cat_image_path):
    """Функция подготовки данных для письма"""

    # Исправление спецсимволов (чтобы не было &#x27; вместо кавычек)
    import html
    cat_name_clean = html.unescape(cat_data["cat_name"])

    subject = f'🐱 Ваш котик "{cat_name_clean}" от Котофабрики'

    text_content = f"""Поздравляем! Ваш котик готов.
Имя: {cat_name_clean}
Состав: {cat_data['head_name']} + {cat_data['body_name']}
"""

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f4f4; padding: 20px; }}
            .container {{ max-width: 600px; margin: 0 auto; background: #ffffff; border-radius: 15px; padding: 30px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }}
            h1 {{ color: #4CAF50; text-align: center; margin-top: 0; }}
            .details {{ background: #f9f9f9; padding: 15px; border-radius: 10px; margin: 20px 0; color: #555; }}
            .footer {{ text-align: center; color: #999; font-size: 12px; margin-top: 30px; }}
            img {{ display: block; margin: 0 auto; max-width: 100%; border-radius: 10px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🐱 Котик готов!</h1>
            <p>Привет, {user.first_name or user.username}!</p>
            <p>Вы только что создали прекрасного котика по имени <strong>{cat_name_clean}</strong>.</p>

            <img src="cid:cat_image" alt="Ваш котик">

            <div class="details">
                <p><strong>Голова:</strong> {cat_data['head_name']}</p>
                <p><strong>Туловище:</strong> {cat_data['body_name']}</p>
            </div>

            <p style="text-align: center;">Спасибо, что играете с нами!</p>

            <div class="footer">
                Котофабрика © {cat_data['created_at']}
            </div>
        </div>
    </body>
    </html>
    """

    return send_email_direct(
        to_email=user.email,
        subject=subject,
        text_content=text_content,
        html_content=html_content,
        image_path=cat_image_path
    )