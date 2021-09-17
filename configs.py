from pathlib import Path
import os
""" Flask application config """

# # Flask settings
# SECRET_KEY = 'This is an INSECURE secret!! DO NOT use this in production!!'
#
# UPLOAD_FOLDER = str(Path.home()) + "/Downloads"
#
# # Flask-SQLAlchemy settings
# SQLALCHEMY_DATABASE_URI = 'sqlite:///drive_db.db'  # File-based SQL database
# SQLALCHEMY_TRACK_MODIFICATIONS = False  # Avoids SQLAlchemy warning

upload_folder = Path.joinpath(Path.home(), "Downloads")
upload_folder = str(Path.home()) if not upload_folder.exists() else upload_folder


# Class-based application configuration
class ConfigClass(object):
    """ Flask application config """

    # Flask settings
    SECRET_KEY = 'This is an INSECURE secret!! DO NOT use this in production!!'
    # SESSION_COOKIE_SECURE = True

    UPLOAD_FOLDER = str(Path.home()) + "/Downloads"

    # Flask-SQLAlchemy settings
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///drive_db.db'  # File-based SQL database
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")   # File-based SQL database
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Avoids SQLAlchemy warning
