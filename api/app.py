"""
Flask API Application
Main entry point for the Terminal Monitoring API
"""
import sys
import os
from flask import Flask, jsonify
from flask_cors import CORS

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api.config import config
from api.routes.metrics import metrics_bp
from api.routes.equipment import equipment_bp
from api.routes.incidents import incidents_bp


def create_app():
    """Application factory"""
    app = Flask(__name__)
    app.config.from_object(config)
    
    # Enable CORS
    CORS(app, origins=config.CORS_ORIGINS)
    
    # Register blueprints
    app.register_blueprint(metrics_bp)
    app.register_blueprint(equipment_bp)
    app.register_blueprint(incidents_bp)
    
    # Health check endpoint
    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({
            'status': 'healthy',
            'service': 'Terminal Monitoring API',
            'version': config.API_VERSION
        }), 200
    
    # API info endpoint
    @app.route('/api', methods=['GET'])
    def api_info():
        return jsonify({
            'title': config.API_TITLE,
            'version': config.API_VERSION,
            'endpoints': {
                'metrics': '/api/metrics/*',
                'equipment': '/api/equipment/*',
                'incidents': '/api/incidents/*'
            }
        }), 200
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(
        host=config.API_HOST if hasattr(config, 'API_HOST') else '0.0.0.0',
        port=config.API_PORT if hasattr(config, 'API_PORT') else 5000,
        debug=config.DEBUG
    )
