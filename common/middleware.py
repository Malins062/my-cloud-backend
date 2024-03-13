import logging
from django.conf import settings
from rest_framework.views import exception_handler

# Устанавливаем уровень логирования в зависимости от DEBUG
if settings.DEBUG:
    log_level = logging.DEBUG
else:
    log_level = logging.INFO

# Конфигурируем логирование
logging.basicConfig(level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)


class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Логирование вызова response
        logger.info(f'Response status: {response.status_code}')

        return response

    def process_exception(self, request, exception):
        # Логирование исключения
        logger.error(f'Exception: {exception}')

        return None

    def app_exception_handler(self, exc, context):
        response = exception_handler(exc, context)

        if response is not None:
            logger.error('{} - {}'.format(response.status_code, response.data))

        return response
