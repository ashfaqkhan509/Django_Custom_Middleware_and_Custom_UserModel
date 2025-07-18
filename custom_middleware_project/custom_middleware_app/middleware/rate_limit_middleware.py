from django.core.cache import cache
from django.http import JsonResponse
import time


class RateLimitMiddleware:

    """
    Rate Limiting Middleware:
    - Block users that are exceeding 5 requests per minute by default.
    - Automatically unblock users after 1 minute.
    - Provide appropriate exception messages.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.RATE_LIMIT = 5
        self.BLOCK_DURATION = 60

    def __call__(self, request):
        
        ip_address = request.META.get('REMOTE_ADDR')
        cache_key = f'rate_limit_{ip_address}'

        request_history = cache.get(cache_key, [])
        current_time = time.time()

        request_history = [time for time in request_history if current_time - time < self.BLOCK_DURATION]

        if len(request_history) >= self.RATE_LIMIT:
            return JsonResponse({
                "error": "Too many requests. rate limit exceed",
            }, status=429)

        request_history.append(current_time)
        cache.set(cache_key, request_history, self.BLOCK_DURATION)
        response = self.get_response(request)
        
        return response