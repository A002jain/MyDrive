from __future__ import print_function
import os
import re
import mimetypes
from flask import (
    Response, Blueprint, redirect, render_template, request, session, url_for
)
from utils import change_dir, provide_dir_path, list_files_to_stream

bp = Blueprint('stream', __name__)

VIDEO_PATH = '/video'
MB = 1 << 20
BUFF_SIZE = 10 * MB
global listFiles


@bp.route('/media', methods=['GET', 'POST'])
def media_video():
    global listFiles
    if 'username' not in session:
        return "login first <a href='/login'>login</a>"
    listFiles = list_files_to_stream()
    return render_template('streamMedia.html', list=listFiles, dirLength=len(listFiles))


@bp.route('/back1', methods=['GET', 'POST'])
def back():
    if 'username' not in session:
        return "login first <a href='/login'>login</a>"
    change_dir("..")
    return redirect(url_for('stream.media_video'))


@bp.route('/stream/<int:file>')
def home(file):
    global listFiles
    print(listFiles[file])
    if listFiles[file].find(".") == -1:
        print("*" * 100)
        change_dir(listFiles[file])
        return redirect(url_for('stream.media_video'))
    response = render_template('streaming.html', video=VIDEO_PATH + "/" + str(file))
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


@bp.route(VIDEO_PATH + "/<int:file>")
def video(file):
    global listFiles
    path = provide_dir_path() + listFiles[file]
    start, end = get_range(request)
    return partial_response(path, start, end)
