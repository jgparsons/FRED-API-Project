# web_app/__init__.py

import os
from flask import Flask
from dotenv import load_dotenv
import app.collect_FRED_data
import app.send_emails

load_dotenv()

def create_app():
    """
    Application factory for the Fed Rate Watch web app.
    Sets up Flask, configuration, and route blueprints.
    """

    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static"
    )

    # SECRET KEY for flash messaging & sessions
    app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret-key")

    # ---- Register route blueprints ---- #
    from .routes.home_routes import home_routes
    app.register_blueprint(home_routes)

    from .routes.rate_updates_routes import rate_updates_routes
    app.register_blueprint(rate_updates_routes)

    from .routes.unsubscribe_routes import unsubscribe_routes
    app.register_blueprint(unsubscribe_routes)

    from .routes.subscribe_routes import subscribe_routes
    app.register_blueprint(subscribe_routes)

    return app


if __name__ == "__main__":
    my_app = create_app()
    my_app.run(debug=True)

app = create_app()
