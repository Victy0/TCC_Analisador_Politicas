"""
WSGI config for privacyPolicyAnalyzer project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
import socketio
from socketServer.views import sio

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'privacyPolicyAnalyzer.settings')

#application = get_wsgi_application()
django_app = get_wsgi_application()
application = socketio.WSGIApp(sio, django_app)