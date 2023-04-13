import os
from whitenoise import WhiteNoise
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.settings')

application = MyWSGIApp()
application = WhiteNoise(application, root="/path/to/static/files")
application.add_files("/path/to/more/static/files", prefix="more-files/")
application = get_wsgi_application()
