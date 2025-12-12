"""
Configuration package for the Crown Nexus System.
"""

from .celery import app as celery_app

__all__ = ("celery_app",)
