from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Application
from .utils import send_telegram_message
import logging

logger = logging.getLogger(__name__)


def index(request):
    return render(request, 'main/index.html')


@require_http_methods(["POST"])
def submit_application(request):
    """
    Обработчик отправки заявки из формы.
    Сохраняет заявку в БД и отправляет уведомление в Telegram.
    """
    try:
        name = request.POST.get('name', '').strip()
        phone = request.POST.get('phone', '').strip()
        
        # Валидация данных
        if not name or not phone:
            return JsonResponse(
                {'success': False, 'message': 'Пожалуйста, заполните все поля'},
                status=400
            )
        
        # Сохранение заявки в БД
        application = Application.objects.create(
            name=name,
            phone=phone
        )
        logger.info(f"Application created: {application.id} - {name}")
        
        # Отправка в Telegram
        telegram_sent = send_telegram_message(name, phone)
        
        if telegram_sent:
            return JsonResponse({
                'success': True,
                'message': 'Спасибо! Мы получили вашу заявку и скоро свяжемся с вами'
            })
        else:
            # Заявка сохранена в БД, но не отправлена в Telegram
            logger.warning(f"Application saved but Telegram notification failed: {application.id}")
            return JsonResponse({
                'success': True,
                'message': 'Спасибо! Мы получили вашу заявку и скоро свяжемся с вами',
                'warning': 'Уведомление в Telegram отправлено с задержкой'
            })
    
    except Exception as e:
        logger.error(f"Error in submit_application: {str(e)}")
        return JsonResponse(
            {'success': False, 'message': 'Произошла ошибка. Пожалуйста, попробуйте позже'},
            status=500
        )
