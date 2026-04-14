import os
from flask import Flask, redirect
from app.config import Config
from utils.logger import get_logger
from app.routes.detection_routes import detection_bp
from app.routes.dashboard_routes import dashboard_bp
from flask_login import LoginManager
from database.models import User
from database.db import SessionLocal

def create_app():
    """
    Application factory (enterprise standard)
    """
    login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    db = SessionLocal()
    return db.query(User).get(int(user_id))

    # ✅ BASE DIR FIX
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    # ✅ STATIC + TEMPLATE FIX (IMPORTANT)
    app = Flask(
        __name__,
        template_folder=os.path.join(BASE_DIR, "dashboard/templates"),
        static_folder=os.path.join(BASE_DIR, "dashboard/static"),
        static_url_path="/dashboard/static"
    )

    # Load configuration
    app.config.from_object(Config)

    # LOGGER SETUP
    logger = get_logger("MainApp")
    app.logger = logger
    logger.info("🚀 Initializing NIDS Application...")

    # REGISTER BLUEPRINTS
    app.register_blueprint(detection_bp, url_prefix="/api")
    app.register_blueprint(dashboard_bp, url_prefix="/dashboard")

    # ROOT REDIRECT
    @app.route("/")
    def home():
        return redirect("/dashboard/")

    # HEALTH CHECK
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

    app.logger.info(f"🌐 Starting server at http://127.0.0.1:{port}")

    app.run(host=host, port=port, debug=debug)
    
