# Ensure apscheduler is installed
try:
    import apscheduler
except ImportError:
    import subprocess
    subprocess.check_call(['pip', 'install', 'apscheduler'])

# Ensure psutil is installed
try:
    import psutil
except ImportError:
    import subprocess
    subprocess.check_call(['pip', 'install', 'psutil'])

from app.core.scheduler import start_scheduler
import os
from app import create_app

app = create_app()

if __name__ == '__main__':
    # Get host and port from environment variables with defaults
    host = os.getenv('FLASK_RUN_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_RUN_PORT', 8000))
    debug = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'

    # Warning: Do not use Flask's built-in server in production
    start_scheduler()

app.run(host=host, port=port, debug=debug)
