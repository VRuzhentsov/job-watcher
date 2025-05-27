from flask import Flask

def create_app():
    """Create and configure the Flask app."""
    app = Flask(__name__)
    
    @app.route('/health')
    def health_check():
        """Health check endpoint for Docker."""
        return {'status': 'healthy'}, 200
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
