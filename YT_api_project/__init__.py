# Import celery app as soon as app is ready
from .celery import app as celery_app

__all__ = ('celery_app',)