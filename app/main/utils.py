import requests
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


def send_telegram_message(name: str, phone: str) -> bool:
    """
    Отправляет сообщение с заявкой в Telegram на все указанные чаты
    
    Args:
        name: Имя клиента
        phone: Номер телефона клиента
        
    Returns:
        bool: True если сообщение отправлено хотя бы в один чат, False иначе
    """
    try:
        if not hasattr(settings, 'TELEGRAM_BOT_TOKEN') or not hasattr(settings, 'TELEGRAM_CHAT_ID'):
            logger.error("Telegram settings not configured")
            return False
        
        bot_token = settings.TELEGRAM_BOT_TOKEN
        chat_ids = settings.TELEGRAM_CHAT_ID
        
        if not bot_token:
            logger.error("TELEGRAM_BOT_TOKEN is empty")
            return False
        
        # Преобразуем в список, если это строка
        if isinstance(chat_ids, str):
            chat_ids = [chat_ids]
        
        if not chat_ids:
            logger.error("TELEGRAM_CHAT_ID is empty")
            return False
        
        # Форматирование сообщения
        message = f"""
🎯 <b>Новая заявка с сайта proPIAR</b>

👤 <b>Имя:</b> {name}
📞 <b>Телефон:</b> {phone}
        """.strip()
        
        # API endpoint для отправки сообщения
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        
        success_count = 0
        
        # Отправляем сообщение в каждый чат
        for chat_id in chat_ids:
            try:
                payload = {
                    "chat_id": chat_id,
                    "text": message,
                    "parse_mode": "HTML"
                }
                
                response = requests.post(url, json=payload, timeout=10)
                
                if response.status_code == 200:
                    logger.info(f"Telegram message sent to chat {chat_id} for {name}")
                    success_count += 1
                else:
                    logger.error(f"Failed to send Telegram message to {chat_id}: {response.text}")
            except Exception as e:
                logger.error(f"Error sending message to chat {chat_id}: {str(e)}")
        
        # Успех, если сообщение отправлено хотя бы в один чат
        return success_count > 0
            
    except Exception as e:
        logger.error(f"Error sending Telegram message: {str(e)}")
        return False
