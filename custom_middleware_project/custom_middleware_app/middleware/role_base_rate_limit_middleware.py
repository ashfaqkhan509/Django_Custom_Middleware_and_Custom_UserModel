import time
from django.core.cache import cache
from django.http import JsonResponse


class RoleBasedRateLimitMiddleware:
    """
    Middleware to enforce rate limits based on user roles.

    Authenticated users are limited by their role:
        - Gold: 10 req/min
        - Silver: 5 req/min
        - Bronze: 2 req/min
        - Others: 1 req/min

    Request timestamps are stored in Django's cache for 60 seconds.
    If a user exceeds their limit, a 429 JSON response is returned.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.BLOCK_DURATION = 60

    def __call__(self, request):
        if not request.user.is_authenticated:
            return self.get_response(request)

        user = request.user
        identity = user.email

        role = getattr(user, 'role', 'bronze')

        role_limits = {
            'gold': 10,
            'silver': 5,
            'bronze': 2
        }

        limit = role_limits.get(role.lower(), 1)

        cache_key = f"role_rl:{identity}"
        request_times = cache.get(cache_key, [])

        current_time = time.time()
        request_times = [time for time in request_times if current_time - time < self.BLOCK_DURATION]

        if len(request_times) >= limit:
            return JsonResponse({
                "error": "Rate limit exceeded",
                "message": f"{role.capitalize()} users are limited to {limit} req/min."
            }, status=429)

        request_times.append(current_time)
        cache.set(cache_key, request_times, timeout=60)

        return self.get_response(request)
