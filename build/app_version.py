import os

VERSION = "2.0.0"
PROJECT_NAME = "FIleDownloader"


def get_project_path():
    # return r"E:WorkSpace\fromUbuntu\Python\pychar_m\FIleDownloader"
    cwd = os.getcwd()
    dir_list = cwd.split("\\")[:-1]
    if PROJECT_NAME == dir_list[-1]:
        dir_list[0] = dir_list[0] + "\\"
        return os.path.join(*dir_list)
    return input("Enter Project Path: ")
