"""
WSGI config for studentstudyportal project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
import sys
import traceback

try:
    from django.core.wsgi import get_wsgi_application
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'studentstudyportal.settings')
    application = get_wsgi_application()
except Exception as e:
    # Log the error for debugging
    print("Error loading application:", str(e))
    traceback.print_exc()
