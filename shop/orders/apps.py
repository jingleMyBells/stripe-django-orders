from django.apps import AppConfig


class OrdersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'orders'

    def ready(self):
        """Добавляем кастомный ресивер сигналов в пространство имен"""
        import orders.signals  # noqa
