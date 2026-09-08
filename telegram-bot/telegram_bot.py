from flask import Flask, request, jsonify
import requests
import os
from datetime import datetime

app = Flask(__name__)

# Telegram конфигурация
TELEGRAM_TOKEN = "8972533630:AAFdVoPpOpSJIX-79vMjBkYaB_fkqqv4PzA"
TELEGRAM_CHAT_ID = "122246714"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

@app.route('/api/quote', methods=['POST'])
def handle_quote():
    try:
        data = request.json

        # Извлечение данных из формы
        project_type = data.get('projectType', 'N/A')
        name = data.get('name', 'N/A')
        phone = data.get('phone', 'N/A')
        email = data.get('email', 'N/A')
        address = data.get('address', 'N/A')
        business_name = data.get('businessName', 'N/A')
        business_address = data.get('businessAddress', 'N/A')
        services = data.get('services', [])
        message = data.get('message', 'N/A')

        # Форматирование сервисов
        services_text = ", ".join(services) if services else "N/A"

        # Создание сообщения для Telegram
        telegram_message = f"""
🏠 НОВАЯ ЗАЯВКА НА КВОТУ

📋 Тип проекта: {project_type.upper()}

👤 Имя: {name}
📞 Телефон: {phone}
📧 Email: {email}

"""

        if project_type == "residential":
            telegram_message += f"🏠 Адрес: {address}\n"
        else:  # commercial
            telegram_message += f"🏢 Компания: {business_name}\n"
            telegram_message += f"📍 Адрес: {business_address}\n"

        telegram_message += f"""
🔧 Услуги: {services_text}

📝 Описание проекта:
{message}

⏰ Время: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}
"""

        # Отправка в Telegram
        response = requests.post(
            TELEGRAM_API_URL,
            json={
                "chat_id": TELEGRAM_CHAT_ID,
                "text": telegram_message,
                "parse_mode": "HTML"
            },
            timeout=10
        )

        if response.status_code == 200:
            return jsonify({
                "success": True,
                "message": "Спасибо за вашу заявку! Мы свяжемся с вами в ближайшее время."
            }), 200
        else:
            print(f"Telegram error: {response.text}")
            return jsonify({
                "success": False,
                "message": "Ошибка при отправке заявки. Пожалуйста, попробуйте позже."
            }), 500

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({
            "success": False,
            "message": f"Ошибка сервера: {str(e)}"
        }), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
