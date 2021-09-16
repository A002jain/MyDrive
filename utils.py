from flask import session
import subprocess as sb
from pathlib import Path
import platform
import os
UPLOAD_FOLDER = str(Path.home()) + "/Downloads"


def get_os():
    return platform.system()


def provide_home_path():
    if get_os() == "Linux":
        return [["File Explorer", str(Path.home()) + "/"], ["External Drive", "/media/"]]
    else:
        try:
            import psutil
            a = psutil.disk_partitions()
            lss = [[], ['External']]
            for i in a:
                if i.fstype == 'NTFS' or i.fstype == 'FAT32':
                    if i.opts == 'rw,fixed':
                        lss[0].append(i.device)
                    else:
                        lss[1].append(i.device)
            # print(lss)
            return lss
        except ImportError:
            dr = 'CDEFGHIJKLMNOPQRSTUVWXYZ'
            hard_drive = [['%s:' % d for d in dr if os.path.exists('%s:' % d)]]
            return hard_drive


# drives = [["File Explorer", str(Path.home()) + "/"], ["External Drive", "/media/"]]
drives = provide_home_path()


def change_dir(directory):
    current_path = provide_dir_path()
    # print("in v2: "+current_path)
    if "switch#Drive" in directory:
        if get_os() == "Linux":
            drives.reverse()
            # print(drives)
            new_path = drives[0][1]
        else:
            index_x = drives[0].index(directory.split("#")[-1]+":\\")
            tmp = drives[0][index_x]
            drives[0][index_x] = drives[0][0]
            drives[0][0] = tmp
            # print(drives[0][0])
            new_path = drives[0][0]
    elif directory != "..":
        new_path = os.path.join(current_path, directory) + "/"
        if not is_dir(new_path):
            new_path = current_path
    else:
        # print("back")
        new_path = str(Path(current_path).parent) + "/"
    # print("new_path: "+new_path)
    set_dir_path(new_path)
    # print("new session path: "+provide_dir_path())
    # return new_path


def provide_dir_path():
    return session['currentPath']


def set_dir_path(path):
    if os.path.exists(path):
        session['currentPath'] = path


def generic_file_listing(path, file_filter=None, view_folder=True):
    # print(path)
    listing = []

    try:
        a = os.scandir(path)
        for i in a:
            if not i.name.startswith("."):
                if file_filter is not None:
                    if i.name[-3:] in file_filter or i.name[-4:] in file_filter:
                        listing.append(i.name)
                    if i.name.find(".") == -1 and view_folder:
                        listing.append(i.name)
                else:
                    listing.append(i.name)
    except FileNotFoundError:
        set_dir_path(drives[0][1])
        generic_file_listing(provide_dir_path())
    return listing


def is_dir(new_path):
    return os.path.isdir(new_path)


"""
Deprecated function below
used in stable 1 commit
Not used after stable 1 commit
"""


"""
this used for converting path which have path like
path = /home/abhinav jain/  --> convert to /home/'abhinav jain'/
path = /home/abhinav jain/Downloads --> convert to /home/'abhinav jain'/Downloads
Instead us os.path.join or os.scandir provided in os module
"""


def provide_ls_cmd():
    current_path = ""
    tmp = session['currentPath']
    s = tmp.split("/")
    for i in s[1:-1]:
        if i.find(" ") != -1:
            current_path = current_path + "/'" + i + "'"
        else:
            current_path = current_path + "/" + i
    current_path = current_path + "/"
    print(current_path)
    print(session['currentPath'])
    return "ls " + current_path


def change_dir_v2(directory):
    current_path = session['currentPath']
    if "switch#Drive" in directory:
        if get_os() == "Linux":
            drives.reverse()
            print(drives)
            session['currentPath'] = drives[0][1]
        else:
            index_x = drives[0].index(directory.split("#")[-1]+":\\")
            tmp = drives[0][index_x]
            drives[0][index_x] = drives[0][0]
            drives[0][0] = tmp
            print(drives[0][0])
            session['currentPath'] = drives[0][0]
    elif directory != "..":
        session['currentPath'] = current_path + directory + "/"
    else:
        print("back")
        current_path = current_path[:-1] if current_path[-1] == "/" else current_path
        tmp = current_path.split("/")[1:-1]
        current_path = ""
        for i in tmp:
            current_path = current_path + "/" + i
        session['currentPath'] = current_path + "/"
    print(provide_dir_path())


def filter_video(file_list):
    files = []
    for i in file_list:
        if i[-3:] == "mp4" or i[-3:] == "mkv":
            files.append(i)
        if i.find(".") == -1:
            files.append(i)
    return files[:-1]


def files_listing():
    files_x = sb.Popen(provide_ls_cmd(), shell=True, stdout=sb.PIPE, stdin=sb.PIPE, stderr=sb.PIPE)
    list_files = files_x.stdout.read().decode().split("\n")[:-1]
    return list_files


def stream_files_listing():
    list_files = filter_video(file_list=files_listing())
    return list_files


def drive_files_listing():
    return files_listing()
