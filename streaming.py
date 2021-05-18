from __future__ import print_function
import os
import re
import mimetypes
from flask import (
    Response, Blueprint, redirect, render_template, request, session, url_for
)
from utils import change_dir, provide_dir_path, generic_file_listing, drives, get_os
from custum_decorators import login_required, check_ban_user
from db_file import get_folder_db_data
stream_bp = Blueprint('stream', __name__)

VIDEO_PATH = '/video'
MB = 1 << 20
BUFF_SIZE = 15 * MB


@stream_bp.before_request
@check_ban_user
def check_user_data():
    pass


@stream_bp.route('/media', methods=['GET', 'POST'])
@login_required
def media_video():
    session['current_video_path'] = session.get('current_video_path')
    is_admin = session['username'] == "admin" and session['verified']
    listFiles = generic_file_listing(path=provide_dir_path(), file_filter=["mp4", "mkv", "webm", "mp3"],
                                     view_folder=True if is_admin else False)
    session['video_list'] = listFiles
    if session['username'] == "admin":
        return render_template('streamMedia.html', list=listFiles, dirLength=len(listFiles),
                               drive_name=drives, os_name=get_os())
    else:
        return render_template('streamMedia.html', list=listFiles, dirLength=len(listFiles), drive_name=drives,
                               folders=get_folder_db_data(enable=True), os_name=get_os())


# @stream_bp.route('/back1', methods=['GET', 'POST'])
# def back():
#     if 'username' not in session:
#         return "login first <a href='/login'>login</a>"
#     change_dir("..")
#     return redirect(url_for('stream.media_video'))


# @stream_bp.route('/switchDrive1/<tag>//')
# @stream_bp.route('/switchDrive1', methods=['GET'])
# @login_required
# def switch_drive(tag=None):
#     if 'username' not in session:
#         return "login first <a href='/login'>login</a>"
#     if tag is None:
#         change_dir("switch#Drive")
#     else:
#         change_dir("switch#Drive#"+str(tag))
#     return redirect(url_for('stream.media_video'))


@stream_bp.route('/stream/<int:tag>')
@login_required
def home(tag=None):
    listFiles = session['video_list']
    if listFiles[tag].find(".") == -1:
        if session['username'] == "admin" and session['verified']:
            change_dir(listFiles[tag])
        return redirect(url_for('stream.media_video'))
    session['current_video_path'] = None
    response = render_template('streaming.html', video=VIDEO_PATH + "/" + str(tag))
    return response


def partial_response(path, start, end=None):
    file_size = os.path.getsize(path)
    # Determine (end, length)
    if end is None:
        end = start + BUFF_SIZE - 1
    end = min(end, file_size - 1)
    end = min(end, start + BUFF_SIZE - 1)
    length = end - start + 1

    # Read file
    with open(path, 'rb') as fd:
        fd.seek(start)
        bytes_x = fd.read(length)
    assert len(bytes_x) == length

    response = Response(
        bytes_x,
        206,
        mimetype=mimetypes.guess_type(path)[0],
        direct_passthrough=True,
    )
    response.headers.add(
        'Content-Range', 'bytes {0}-{1}/{2}'.format(
            start, end, file_size,
        ),
    )
    response.headers.add(
        'Accept-Ranges', 'bytes'
    )
    return response


def get_range(request_x):
    range_x = request_x.headers.get('Range')
    m = re.match('bytes=(?P<start>\d+)-(?P<end>\d+)?', range_x)
    if m:
        start = m.group('start')
        end = m.group('end')
        start = int(start)
        if end is not None:
            end = int(end)
        return start, end
    else:
        return 0, None


@stream_bp.route(VIDEO_PATH + "/<int:file>")
def video(file=None):
    if 'username' not in session:
        return redirect(url_for('user.login'))
    listFiles = session["video_list"]
    if session['current_video_path'] is None:
        session['current_video_path'] = provide_dir_path() + listFiles[file]
    path = session['current_video_path']
    start, end = get_range(request)
    return partial_response(path, start, end)
