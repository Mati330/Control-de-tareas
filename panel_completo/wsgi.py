import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'panel_completo.settings')  # Reemplaza 'tu_proyecto' con el nombre de tu proyecto

application = get_wsgi_application()