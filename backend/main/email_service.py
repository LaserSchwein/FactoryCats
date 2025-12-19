import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import logging
import os

logger = logging.getLogger(__name__)


def send_email_direct(to_email, subject, text_content, html_content=None, image_path=None):
    try:
        # Настройки SMTP
        smtp_server = "smtp.yandex.ru"
        port = 587
        sender_email = "cotofabrica@yandex.ru"
        password = "dvqhcxuijzzhrsbt"

        # Создаем сообщение
        msg = MIMEMultipart('related')
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = to_email
        msg['Reply-To'] = sender_email

        # Текстовая часть
        text_part = MIMEText(text_content, 'plain', 'utf-8')
        msg.attach(text_part)

        # HTML часть (если есть)
        if html_content:
            html_part = MIMEText(html_content, 'html', 'utf-8')
            msg.attach(html_part)

        # Изображение (если есть)
        if image_path and os.path.exists(image_path):
            try:
                with open(image_path, 'rb') as f:
                    img_data = f.read()

                image = MIMEImage(img_data)
                image.add_header('Content-ID', '<cat_image>')
                image.add_header('Content-Disposition', 'inline', filename='cat.png')
                msg.attach(image)
            except Exception as e:
                logger.warning(f"Не удалось прикрепить изображение: {e}")

        # Создаем SMTP соединение
        server = smtplib.SMTP(smtp_server, port, timeout=30)

        # Включаем TLS
        server.starttls()

        # Логинимся
        server.login(sender_email, password)

        # Отправляем
        server.send_message(msg)

        # Закрываем соединение
        server.quit()

        logger.info(f"✅ Письмо отправлено на {to_email}")
        return True

    except Exception as e:
        logger.error(f"❌ Ошибка отправки на {to_email}: {str(e)}")
        return False


def send_cat_email(user, cat_data, cat_image_path):
    subject = f'🐱 Ваш котик "{cat_data["cat_name"]}" от Котофабрики'

    # Текстовое сообщение
    text_content = f"""Ваш новый котик от Котофабрики!

Имя: {cat_data['cat_name']}
Голова: {cat_data['head_name']}
Тело: {cat_data['body_name']}
Дата создания: {cat_data.get('created_at', '')}

Изображение котика прикреплено к письму.

С уважением, команда Котофабрики 🐱"""

    # HTML сообщение
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
</head>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
        <h1 style="color: #4CAF50;">🐱 Ваш котик "{cat_data['cat_name']}" от Котофабрики!</h1>

        <p>Привет, {user.first_name or 'друг'}!</p>

        <p>Вы создали уникального котика в нашем конструкторе. Вот детали:</p>

        <div style="background: #f9f9f9; padding: 15px; border-radius: 8px; margin: 20px 0;">
            <p><strong>Имя:</strong> {cat_data['cat_name']}</p>
            <p><strong>Голова:</strong> {cat_data['head_name']}</p>
            <p><strong>Тело:</strong> {cat_data['body_name']}</p>
            <p><strong>Дата создания:</strong> {cat_data.get('created_at', '')}</p>
        </div>

        <p>Изображение котика прикреплено к этому письму. Сохраните его!</p>

        <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee; color: #666;">
            <p>С уважением, команда Котофабрики 🐱</p>
            <p><small>Это письмо отправлено автоматически. Пожалуйста, не отвечайте на него.</small></p>
        </div>
    </div>
</body>
</html>"""

    # Отправляем письмо
    return send_email_direct(
        to_email=user.email,
        subject=subject,
        text_content=text_content,
        html_content=html_content,
        image_path=cat_image_path
    )