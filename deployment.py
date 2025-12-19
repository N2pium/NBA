import os
import sys
from pathlib import Path

# Set the project base directory
BASE_DIR = Path(__file__).resolve().parent

# Add the 'website' subdirectory (which contains the actual Django project) to the Python path
# This allows us to do "from website import settings" even if we are in the root directory
sys.path.insert(0, str(BASE_DIR / 'website'))

# Set the default settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
