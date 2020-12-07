from flask import session
import subprocess as sb
import os

drives = [["File Explorer", "/home/abhinav/"], ["External Drive", "/media/abhinav/"]]
userList = [["Abhinav Jain", "q"], ["har", "q"]]
uploadPageSwitch = True


def change_dir(directory):
    print("hello")
    current_path = session['currentPath']
    if directory == "switchDrive":
        drives.reverse()
        print(drives)
        session['currentPath'] = drives[0][1]
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


def provide_dir_path():
    return session['currentPath']


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


def get_os():
    return os.uname().sysname


def filter_video(file_list):
    files = []
    f = file_list.stdout.read().decode()
    ff = f.split("\n")
    for i in ff:
        if i[-3:] == "mp4" or i[-3:] == "mp3":
            files.append(i)
        if i.find(".") == -1:
            files.append(i)
    return files[:-1]


def generic_file_listing(path):
    listing = []
    a = os.scandir(path)
    for i in a:
        if not i.name.startswith("."):
            listing.append(i.name)
    return listing


def list_files_to_stream():
    files_x = sb.Popen(provide_ls_cmd(), shell=True, stdout=sb.PIPE, stdin=sb.PIPE, stderr=sb.PIPE)
    #    listFiles = files_x.stdout.read().decode().split("\n")[:-1]
    listFiles = filter_video(files_x)
    return listFiles


def drive_listing():
    files_x = sb.Popen(provide_ls_cmd(), shell=True, stdout=sb.PIPE, stdin=sb.PIPE, stderr=sb.PIPE)
    list_files = files_x.stdout.read().decode().split("\n")[:-1]
    return list_files


def generic_list_files():
    pass
