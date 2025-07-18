from django.test import TestCase, RequestFactory
from unittest.mock import patch, MagicMock
from django.http import HttpResponse
from custom_middleware_app.middleware.logging_middleware import RequestLoggerMiddleware
from custom_middleware_app.middleware.rate_limit_middleware import RateLimitMiddleware
from custom_middleware_app.middleware.role_base_rate_limit_middleware import (
    RoleBasedRateLimitMiddleware
)
import time
from django.core.cache import cache


class RequestLoggerMiddlewareTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        # A simple dummy view to pass through middleware
        def get_response(request):
            return HttpResponse("OK")

        self.middleware = RequestLoggerMiddleware(get_response)

    @patch("custom_middleware_app.middleware.logging_middleware.logger.info")
    def test_logs_ip_and_method_with_forwarded_for(self, mock_logger):
        request = self.factory.get("/", HTTP_X_FORWARDED_FOR="203.0.113.1")
        response = self.middleware(request)

        self.assertEqual(response.status_code, 200)
        mock_logger.assert_called_with("IP: 203.0.113.1, Method: GET")

    @patch("custom_middleware_app.middleware.logging_middleware.logger.info")
    def test_logs_ip_and_method_with_remote_addr(self, mock_logger):
        request = self.factory.post("/", REMOTE_ADDR="198.51.100.1")
        response = self.middleware(request)

        self.assertEqual(response.status_code, 200)
        mock_logger.assert_called_with("IP: 198.51.100.1, Method: POST")


class RateLimitMiddlewareTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        # A simple dummy view to pass through middleware
        def get_response(request):
            return HttpResponse("OK")

        self.middleware = RateLimitMiddleware(get_response)
        
        cache.clear()

    def test_allows_requests_under_limit(self):
        """
        Should allow requests if under the limit.
        """
        request = self.factory.get("/", REMOTE_ADDR="127.0.0.1")
        response = self.middleware(request)
        self.assertEqual(response.status_code, 200)

    def test_blocks_requests_over_limit(self):
        """
        Should block requests when limit is exceeded.
        """
        ip = "127.0.0.1"
        request = self.factory.get("/", REMOTE_ADDR=ip)

        # Make 5 allowed requests
        for _ in range(5):
            self.middleware(request)

        # 6th request should be blocked
        response = self.middleware(request)
        self.assertEqual(response.status_code, 429)
        self.assertIn(b"Too many requests", response.content)

    def test_unblocks_after_block_duration(self):
        """
        Should unblock after BLOCK_DURATION seconds.
        """
        ip = "127.0.0.1"
        request = self.factory.get("/", REMOTE_ADDR=ip)

        # Hit the limit
        for _ in range(5):
            self.middleware(request)

        # Wait for block duration to expire
        time.sleep(self.middleware.BLOCK_DURATION)

        response = self.middleware(request)
        self.assertEqual(response.status_code, 200)


class RoleBasedRateLimitMiddlewareTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        cache.clear()

        # A simple get_response that returns "OK"
        def get_response(request):
            return HttpResponse("OK")
        self.middleware = RoleBasedRateLimitMiddleware(get_response)

        # Mock user
        self.user = MagicMock()
        self.user.email = "test@example.com"
        self.user.is_authenticated = True

    def test_allows_request_under_limit(self):
        """
        Should allow requests when under the rate limit.
        """
        self.user.role = "gold"
        request = self.factory.get("/")
        request.user = self.user

        response = self.middleware(request)
        self.assertEqual(response.status_code, 200)

    def test_blocks_requests_over_limit(self):
        """
        Should block requests when limit is exceeded.
        """
        self.user.role = "bronze"  # limit = 2 req/min
        request = self.factory.get("/")
        request.user = self.user

        # Make 2 allowed requests
        self.middleware(request)
        self.middleware(request)

        # Third should be blocked
        response = self.middleware(request)
        self.assertEqual(response.status_code, 429)
        self.assertIn("Rate limit exceeded", response.content.decode())

    def test_resets_after_60_seconds(self):
        """Should allow new requests after 60 seconds."""
        self.user.role = "bronze"
        request = self.factory.get("/")
        request.user = self.user

        self.middleware(request)
        self.middleware(request)

        with patch("time.time", return_value=time.time() + 61):
            response = self.middleware(request)

        self.assertEqual(response.status_code, 200)

    def test_non_authenticated_user_bypasses_limit(self):
        """Non-authenticated users are not rate-limited by this middleware."""
        request = self.factory.get("/")
        request.user = MagicMock(is_authenticated=False)

        response = self.middleware(request)
        self.assertEqual(response.status_code, 200)