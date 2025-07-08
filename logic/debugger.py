import os
import logging
from django.conf import settings
from django.urls import resolve, Resolver404
from django.db import connection, OperationalError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%H:%M:%S'
)

DEBUG_MODE = True

# 1. General debug logger

def debug(message, level='info'):
    """
    Log a debug message with optional logging level.
    """
    if DEBUG_MODE:
        prefix = "🛠️ DEBUG"
        print(f"{prefix} | {message}")
        if level == 'info':
            logging.info(message)
        elif level == 'warning':
            logging.warning(message)
        elif level == 'error':
            logging.error(message)

# 2. Template existence check
def check_template_exists(template_relative_path):
    """
    2. Check if a Django template exists in the templates directory.
    """
    template_path = os.path.join(settings.BASE_DIR, "templates", template_relative_path)
    if os.path.exists(template_path):
        debug(f"2. ✅ Template exists: {template_relative_path}")
    else:
        debug(f"2. ⚠️ Template not found: {template_relative_path}", level='warning')

# 3. URL resolution check
def check_url_resolves(url_path):
    """
    3. Check if a URL path resolves to a view.
    """
    try:
        match = resolve(url_path)
        debug(f"3. ✅ URL resolved: {url_path} -> view '{match.view_name}'")
    except Resolver404:
        debug(f"3. ⚠️ URL not resolved: {url_path}", level='warning')

# 4. Database connectivity check
def check_db_connection():
    """
    4. Ensure the database connection is working.
    """
    try:
        connection.ensure_connection()
        debug("4. ✅ Database connection successful")
    except OperationalError as e:
        debug(f"4. ⚠️ Database connection failed: {e}", level='error')

# 5. Table existence check
def check_table_exists(table_name):
    """
    5. Check if a specific table exists in the database.
    """
    tables = connection.introspection.table_names()
    if table_name in tables:
        debug(f"5. ✅ Table exists: {table_name}")
    else:
        debug(f"5. ⚠️ Table missing: {table_name}", level='warning')

# 6. Static file existence check
def check_static_file(relative_path):
    """
    6. Check if a static file exists under the static directory.
    """
    static_path = os.path.join(settings.BASE_DIR, "static", relative_path)
    if os.path.exists(static_path):
        debug(f"6. ✅ Static file exists: {relative_path}")
    else:
        debug(f"6. ⚠️ Static file missing: {relative_path}", level='warning')

# 7. Environment variable check
def check_env_var(var_name):
    """
    7. Check if an environment variable is set.
    """
    val = os.getenv(var_name)
    if val is not None:
        debug(f"7. ✅ Env var '{var_name}' = '{val}'")
    else:
        debug(f"7. ⚠️ Env var '{var_name}' is not set", level='warning')
