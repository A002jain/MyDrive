from flask import Flask
from db_instance import db
from streaming import stream_bp
from users import user_bp
from drive import drive_bp
from admin_panel import admin_bp
from configs import ConfigClass
from commands import *


def create_app():
    """ Flask application factory """

    # Create Flask app load app.config
    app = Flask(__name__)
    app.config.from_object(ConfigClass)
    # app.config.from_pyfile("configs.py")
    # adding user Blueprint
    app.register_blueprint(admin_bp)
    app.register_blueprint(stream_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(drive_bp)
    # Initialize Flask-SQLAlchemy
    db.init_app(app)

    # Create all database tables
    # with app.app_context():
    #     db.drop_all()
    #     db.create_all()
    app.cli.add_command(init_db)
    app.cli.add_command(reset_db)
    app.cli.add_command(add_admin)
    return app

