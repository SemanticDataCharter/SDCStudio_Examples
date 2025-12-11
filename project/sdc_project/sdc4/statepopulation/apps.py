"""
Django app configuration for statepopulation.
"""
from django.apps import AppConfig


class StatepopulationConfig(AppConfig):
    """App configuration for statepopulation."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'statepopulation'

    def ready(self):
        """
        Import signals when app is ready.

        This ensures that signal handlers are registered when Django starts.
        """
        import statepopulation.signals  # noqa: F401
