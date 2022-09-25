import os
import shutil
import platform

# noinspection PyUnresolvedReferences
from app_version import VERSION, get_project_path

"""
old linux stable
if __name__ == '__main__':
    folder = f"v_{VERSION}"
    if not os.path.exists(folder):
        os.mkdir(folder)
        os.chdir(folder)
        os.system("bash ../deployBinary.sh")
        if os.system("./dist/app_runner/app_runner -v") == 0:
            print(f"App Version Updated {VERSION}")
        else:
            print(f"Failed to build {VERSION}")
    else:
        print(f"version: {VERSION} already exist\nUpdate version")
"""

PROJECT_PATH = r"E:\Workspace\Python\MyDrive"
# PROJECT_PATH = get_project_path()
STATIC_FOLDER_PATH = os.path.join(PROJECT_PATH, "static")
TEMPLATE_FOLDER_PATH = os.path.join(PROJECT_PATH, "templates")
RUNNER_FILE = os.path.join(PROJECT_PATH, "app_runner.py")


def build_package():
    tag = input("build tag: ")
    os_system = platform.system()
    os_arch = platform.architecture()[0]
    folder = f"v_{VERSION}_{os_system}_{os_arch}{tag}"
    if not os.path.exists(folder):
        os.mkdir(folder)
        os.chdir(folder)
        folder_seperator = ";" if os_system == "Windows" else ":"
        build_cmd = f"pyinstaller  --add-data {STATIC_FOLDER_PATH}{folder_seperator}static --add-data {TEMPLATE_FOLDER_PATH}{folder_seperator}templates {RUNNER_FILE}"
        print(build_cmd)
        os.system(build_cmd)
        app_runner = os.path.join(os.getcwd(), "dist", "app_runner", "app_runner")
        if os.system(f"{app_runner} -v") != 0:
            print(f"Failed to build {VERSION}")
    else:
        print(f"version: {VERSION} already exist")
        if input("Enter y for build: ") == "y":
            shutil.rmtree(folder)
            build_package()


if __name__ == '__main__':
    build_package()
