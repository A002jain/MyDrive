from app_config import create_app
import argparse

VERSION = "1.9.0"
parser = argparse.ArgumentParser("Start your own Media Server")
parser.add_argument("-v", "--version", help="App version", action="store_true")
parser.add_argument("--host", help="Host IP", metavar="", default="127.0.0.1")
parser.add_argument("-p", "--port", help="Port number", metavar="", default="5000")


if __name__ == '__main__':
    args = parser.parse_args()
    if args.version:
        print(f"App Version {VERSION}")
    else:
        app = create_app()
        host = args.host
        port = args.port
        app.run(host=host, port=port, debug=True)
