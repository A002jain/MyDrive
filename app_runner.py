from app_config import create_app
from app_cli import reset_app, update_admin, verify_admin
import argparse

VERSION = "1.9.9"
parser = argparse.ArgumentParser("Start your own Media Server")
parser.add_argument("-v", "--version", help="App version", action="store_true")
parser.add_argument("--host", help="Host IP", metavar="", default="127.0.0.1")
parser.add_argument("-p", "--port", help="Port number", metavar="", default="5000")
parser.add_argument("--debug", help="debug mode(dev only)", action="store_true")
parser.add_argument("--set_admin", help="create admin user", action="store_true")
parser.add_argument("--reset", help="Reset Database", action="store_true")

if __name__ == '__main__':
    verified = False
    args = parser.parse_args()
    app = create_app()
    if args.version:
        print(f"App Version {VERSION}")
    elif args.debug:
        # do not push it please
        verified = True
    else:
        with app.app_context():
            if verify_admin():
                if not args.reset and not args.set_admin:
                    verified = True
                if args.reset:
                    reset_app()
                elif args.set_admin:
                    update_admin()
            else:
                verified = False
    if verified:
        app.run(host=args.host, port=args.port, debug=args.debug)
        # app.run(host=args.host, port=args.port)
