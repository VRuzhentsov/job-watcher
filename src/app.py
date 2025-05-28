import os
import logging
import sys
import time
import threading
from pathlib import Path
import sentry_sdk
from flask import Flask
from models import db, init_db
from services.telegram import run_bot
from utils import log_version

# Configure logging for Docker containers
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout,
    force=True
)

logger = logging.getLogger(__name__)

# Log version on startup
log_version()

debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
sentry_dsn = os.getenv('SENTRY_DSN')
logger.info(f"Debug mode: {debug_mode}")

def create_app():
    """Create Flask app for health checks and database migrations"""
    logger.info("Creating Flask app...")
    app = Flask(__name__)

    if sentry_dsn:
        sentry_sdk.init(
            dsn=sentry_dsn,
            send_default_pii=True,
            environment=os.getenv('FLASK_ENV', 'production'),
        )

    try:
        db, migrate = init_db(app)
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        sys.stdout.flush()
        raise

    @app.route('/health')
    def health_check():
        return {'status': 'healthy'}, 200

    return app, db, migrate

def watch_files():
    """File watcher for auto-reload in development"""
    if not debug_mode:
        return
        
    logger.info("Starting file watcher for auto-reload")
    src_dir = Path('src')
    if not src_dir.exists():
        src_dir = Path('/app/src')  # Docker path
    
    # Get initial modification times
    file_times = {}
    for py_file in src_dir.rglob('*.py'):
        try:
            file_times[py_file] = py_file.stat().st_mtime
        except OSError:
            continue
    
    while True:
        try:
            time.sleep(1)  # Check every second
            for file_path, last_time in list(file_times.items()):
                try:
                    if file_path.exists():
                        current_time = file_path.stat().st_mtime
                        if current_time > last_time:
                            logger.info(f"File changed: {file_path}")
                            logger.info("Exiting for restart...")
                            os._exit(0)  # Force exit to trigger container restart
                except OSError:
                    continue
                    
            # Check for new files
            for py_file in src_dir.rglob('*.py'):
                if py_file not in file_times:
                    try:
                        file_times[py_file] = py_file.stat().st_mtime
                        logger.info(f"New file detected: {py_file}")
                        logger.info("Exiting for restart...")
                        os._exit(0)
                    except OSError:
                        continue
                        
        except Exception as e:
            logger.error(f"File watcher error: {e}")
            time.sleep(5)  # Wait longer on error

if __name__ == '__main__':
    logger.info("=== Starting Jobs Watcher Application ===")
    
    # Initialize database and Flask app
    app, db, migrate = create_app()
    logger.info("Database initialized")
    
    # Start Flask server in background thread for health checks
    flask_thread = threading.Thread(
        target=lambda: app.run(host='0.0.0.0', port=5000, debug=debug_mode, use_reloader=False),
        daemon=True
    )
    flask_thread.start()
    logger.info("Flask server started for health checks")
    
    # Start file watcher in development mode
    if debug_mode:
        watcher_thread = threading.Thread(target=watch_files, daemon=True)
        watcher_thread.start()
        logger.info("File watcher started")
    
    # Run Telegram bot in main thread
    logger.info("Starting Telegram bot...")
    try:
        run_bot()
    except KeyboardInterrupt:
        logger.info("Application stopped by user")
    except Exception as e:
        logger.error(f"Application error: {e}")
        sys.exit(1)
