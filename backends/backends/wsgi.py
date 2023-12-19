"""
WSGI config for backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

<<<<<<< HEAD
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
=======
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backends.settings')
>>>>>>> d717f5d4ffb90cfb12c5bd52259361ce19ef6e18

application = get_wsgi_application()
