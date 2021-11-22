web: gunicorn   privacyPolicyAnalyzer.wsgi:django_app
web2: daphne privacyPolicyAnalyzer.asgi:application
worker: python3 manage.py runworker channel_layer -v2