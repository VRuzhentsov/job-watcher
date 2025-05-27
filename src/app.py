import os
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from flask import Flask

def create_app():
    """Create and configure the Flask app."""
    app = Flask(__name__)

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
    # In production, disable debug mode to ensure Sentry works properly
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=5000, debug=debug_mode)
