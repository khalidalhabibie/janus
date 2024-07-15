from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint
from flask_migrate import Migrate
from .scheduler import start_scheduler
from .db import db
from .mail import mail


def create_app():
    app = Flask(__name__, static_folder='static', static_url_path='/static')

    app.config.from_object('config.Config')

    db.init_app(app)
    mail.init_app(app)
    Migrate(app, db)

    from .models import Event

    # Swagger UI configuration
    swagger_ui_blueprint = get_swaggerui_blueprint(
        '/api/docs',
        '/swagger/swagger.yaml',
        config={'app_name': "Email Scheduler API"}
    )
    app.register_blueprint(swagger_ui_blueprint)

    from .routes import main
    app.register_blueprint(main)

    with app.app_context():
        start_scheduler(app)

    return app
