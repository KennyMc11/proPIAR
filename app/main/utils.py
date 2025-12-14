import requests
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


def send_telegram_message(name: str, phone: str) -> bool:
    """
    Отправляет сообщение с заявкой в Telegram
    
    Args:
        name: Имя клиента
        phone: Номер телефона клиента
        
    Returns:
        bool: True если сообщение отправлено успешно, False иначе
    """
    try:
        if not hasattr(settings, 'TELEGRAM_BOT_TOKEN') or not hasattr(settings, 'TELEGRAM_CHAT_ID'):
            logger.error("Telegram settings not configured")
            return False
        
        bot_token = settings.TELEGRAM_BOT_TOKEN
        chat_id = settings.TELEGRAM_CHAT_ID
        
        if not bot_token or not chat_id:
            logger.error("TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID is empty")
            return False
        
        # Форматирование сообщения
        message = f"""
🎯 <b>Новая заявка с сайта proPIAR</b>

👤 <b>Имя:</b> {name}
📞 <b>Телефон:</b> {phone}
        """.strip()
        
        # API endpoint для отправки сообщения
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        
        payload = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "HTML"
        }
        
        response = requests.post(url, json=payload, timeout=10)
        
        if response.status_code == 200:
            logger.info(f"Telegram message sent successfully for {name}")
            return True
        else:
            logger.error(f"Failed to send Telegram message: {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"Error sending Telegram message: {str(e)}")
        return False
