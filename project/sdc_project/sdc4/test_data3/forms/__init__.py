"""
Forms for test_data3 wizard.

Each step has its own form class for validation and processing.
"""
from .setup import SetupForm
from .context import ContextForm
from .data_entry import DataEntryForm
from .review import ReviewForm

__all__ = [
    'SetupForm',
    'ContextForm',
    'DataEntryForm',
    'ReviewForm',
]
