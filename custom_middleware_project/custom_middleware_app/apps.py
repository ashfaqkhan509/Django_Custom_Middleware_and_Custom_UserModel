from django.apps import AppConfig


class CustomMiddlewareAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'custom_middleware_app'
