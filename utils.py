from flask import session

drives = [["File Explorer", "/home/abhinav"], ["External Drive", "/media/abhinav"]]
userList = [["Abhinav Jain", "q"], ["har", "q"]]
uploadPageSwitch = True


def change_dir(directory):
    print("hello")
    current_drive = session['currentDrive']
    if directory == "switchDrive":
        drives.reverse()
        print(drives)
        session['currentDrive'] = drives[0][1]
    elif directory != "..":
        session['currentDrive'] = current_drive + "/" + directory
    else:
        print("back")
        current_drive = current_drive[:-1] if current_drive[-1] == "/" else current_drive
        tmp = current_drive.split("/")[1:-1]
        current_drive = ""
        for i in tmp:
            current_drive = current_drive + "/" + i
            session['currentDrive'] = current_drive


def provide_dir_path():
    return session['currentDrive']
