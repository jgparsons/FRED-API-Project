# app/web_app/__init__.py

import os
from flask import Flask
from dotenv import load_dotenv

# Load environment variables (MAILGUN, FRED API KEY, SECRET KEY, etc.)
load_dotenv()

def create_app():
    """
    Application factory for the Fed Rate Watch web app.
    Sets up Flask, configuration, and route blueprints.
    """

    app = Flask(
        __name__,
        template_folder="templates",  # where HTML files live
        static_folder="static"       # if you add CSS/images
    )

    # SECRET KEY for flash messages, sessions, CSRF
    app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret-key")

    # ---- Register route blueprints ---- #
    from .routes.home_routes import home_routes
    app.register_blueprint(home_routes)

    # ---- More blueprints can plug in later ---- #
    # from .routes.rates_routes import rates_routes
    # app.register_blueprint(rates_routes)

    return app
