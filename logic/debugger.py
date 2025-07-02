import os
import logging
from django.conf import settings

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%H:%M:%S'
)

DEBUG_MODE = True

def debug(message):
    if DEBUG_MODE:
        print(f"🛠️ DEBUG | {message}")
        logging.info(message)

def check_template_exists(template_relative_path):
    template_path = os.path.join(settings.BASE_DIR, "templates", template_relative_path)
    if not os.path.exists(template_path):
        debug(f"⚠️ Template not found: {template_relative_path}")
    else:
        debug(f"✅ Template exists: {template_relative_path}")
