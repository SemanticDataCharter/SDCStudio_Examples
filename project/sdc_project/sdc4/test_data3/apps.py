"""
Django app configuration for test_data3.
"""
from django.apps import AppConfig


class Test_data3Config(AppConfig):
    """App configuration for test_data3."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'test_data3'

    def ready(self):
        """
        Import signals when app is ready.

        This ensures that signal handlers are registered when Django starts.
        """
        import test_data3.signals  # noqa: F401
