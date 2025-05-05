# Ensure psutil is installed
try:
    import psutil
except ImportError:
    import subprocess
    import sys
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'psutil'])
        import psutil
    except Exception as e:
        print(f"Failed to install psutil: {e}")
        sys.exit(1)

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
