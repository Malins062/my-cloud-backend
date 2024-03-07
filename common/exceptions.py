from rest_framework.views import exception_handler
import logging

logger = logging.getLogger(__name__)


def app_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        logger.error('{} - {}'.format(response.status_code, response.data))

    return response
