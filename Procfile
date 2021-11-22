web: gunicorn   privacyPolicyAnalyzer.wsgi:django_app
web2: daphne -u /tmp/daphne.sock --access-log - --proxy-headers channelServer.routing