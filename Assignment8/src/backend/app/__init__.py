from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    JWTManager(app)
    
    # Ensure data directory exists
    os.makedirs('data', exist_ok=True)
    
    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.knowledge import knowledge_bp
    from app.routes.search import search_bp
    from app.routes.cluster import cluster_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(knowledge_bp, url_prefix='/api/knowledge')
    app.register_blueprint(search_bp, url_prefix='/api/search')
    app.register_blueprint(cluster_bp, url_prefix='/api/cluster')
    
    return app
