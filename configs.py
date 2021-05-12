from pathlib import Path
""" Flask application config """

# Flask settings
SECRET_KEY = 'This is an INSECURE secret!! DO NOT use this in production!!'

UPLOAD_FOLDER = str(Path.home()) + "/Downloads"
