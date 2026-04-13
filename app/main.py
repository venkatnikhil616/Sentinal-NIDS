import os
from flask import Flask, redirect
from app.config import Config
from utils.logger import get_logger
from app.routes.detection_routes import detection_bp
from app.routes.dashboard_routes import dashboard_bp


def create_app():
    """
    Application factory (enterprise standard)
    """
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(Config)

    # LOGGER SETUP
    
    logger = get_logger("MainApp")
    app.logger = logger
    logger.info("🚀 Initializing NIDS Application...")

    # REGISTER BLUEPRINTS
  
    # Detection API → /api
    app.register_blueprint(detection_bp, url_prefix="/api")

    # Dashboard → /dashboard
    app.register_blueprint(dashboard_bp, url_prefix="/dashboard")

    # ROOT REDIRECT 

    @app.route("/")
    def home():
        return redirect("/dashboard/")

    # HEALTH CHECK (PRODUCTION)
    
    @app.route("/health", methods=["GET"])
    def health_check():
        return {
            "status": "running",
            "service": "NIDS",
            "version": "1.0"
        }, 200

    logger.info("✅ Application setup completed")
    return app
  
# RUN SERVER

if __name__ == "__main__":
    app = create_app()

    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("DEBUG", "True") == "True"

    app.logger.info(f"🌐 Starting server at http://{host}:{port}")

    app.run(host=host, port=port, debug=debug)
