import os
import logging
import sys
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from flask import Flask
from models import db, init_db
from services.telegram import run_bot

# Configure logging for Docker containers
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout,
    force=True
)

logger = logging.getLogger(__name__)

def create_app():
    """Create and configure the Flask app."""
    app = Flask(__name__)
    
    # Initialize database and migrations
    db, migrate = init_db(app)

    sentry_dsn = os.getenv('SENTRY_DSN')
    if sentry_dsn:
        sentry_sdk.init(
            dsn=sentry_dsn,
            send_default_pii=True,
            environment=os.getenv('FLASK_ENV', 'production'),
        )

    @app.route('/health')
    def health_check():
        """Health check endpoint for Docker."""
        return {'status': 'healthy'}, 200

    return app

app = create_app()

if __name__ == '__main__':
    import threading
    
    # Start Flask app in a separate thread
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    flask_thread = threading.Thread(
        target=lambda: app.run(host='0.0.0.0', port=5000, debug=debug_mode, use_reloader=False),
        daemon=True
    )
    flask_thread.start()
    logger.info("Flask app started in background thread")
    
    # Run Telegram bot in main thread (avoids asyncio threading issues)
    logger.info("Starting Telegram bot in main thread...")
    run_bot()
