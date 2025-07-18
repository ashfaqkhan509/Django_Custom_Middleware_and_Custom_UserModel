import logging
from django.utils import timezone

logger = logging.getLogger(__name__)

# Logging Middleware
class RequestLoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """
        Middleware to Capture and log the IP address and request time of each incoming request.
        """
        response = self.get_response(request)
        ip_address = self.get_user_ip(request)
        logger.info(f"IP: {ip_address}, Method: {request.method}")

        return response

    def get_user_ip(self, request):
        """
        Get the IP address of incoming request
        """
        ip_address = request.META.get('HTTP_X_FORWARDED_FOR')
        if ip_address:
            ip_address = ip_address.split(',')[0]
        else:
            ip_address = request.META.get('REMOTE_ADDR')
        return ip_address
