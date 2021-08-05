"""Application entry point"""
from flask import Flask
import os
import logging

logging.basicConfig(
    filename="logs/logging.log",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
)
logging.getLogger("pytorch").setLevel(logging.WARNING)
logging.getLogger("transformers").setLevel(logging.WARNING)


def _initialize_blueprints(app: Flask) -> None:
    """Register Flask blueprints"""
    from app.routes.health_check import health_check
    from app.routes.sentiment_analysis import sentiment_analysis

    app.register_blueprint(health_check)
    app.register_blueprint(sentiment_analysis)


def create_app(is_prod=False) -> Flask:
    """Create an app by initializing components"""
    app: Flask = Flask(__name__, instance_relative_config=True)

    if is_prod == True:
        # Using a production configuration
        app.config.from_pyfile("prod.config.py")
        print("__loading production config__")
    else:
        # Using a development configuration
        app.config.from_pyfile("dev.config.py")
        print("__loading development config__")

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    _initialize_blueprints(app)
    return app
