from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask import Response
from flask import send_from_directory
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db
from datetime import datetime
import base64, json
from io import BytesIO
import os
from PIL import Image
import re
from io import StringIO
import pyautogui

bp = Blueprint("blog", __name__, static_folder='static')
basedir = os.path.abspath(os.path.dirname(__file__))

@bp.route("/")
def index():
    """Show all the posts, most recent first."""
    db = get_db()
    posts = db.execute(
        "SELECT p.id, title, body, created, author_id, username"
        " FROM post p JOIN user u ON p.author_id = u.id"
        " ORDER BY created DESC"
    ).fetchall()
    return render_template("blog/index.html", posts=posts)

# @bp.after_request
# def add_header(r):
#     """
#     Add headers to both force latest IE rendering engine or Chrome Frame,
#     and also to cache the rendered page for 10 minutes.
#     """
#     r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
#     r.headers["Pragma"] = "no-cache"
#     r.headers["Expires"] = "0"
#     r.headers['Cache-Control'] = 'public, max-age=0'
#     return r

def get_post(id, check_author=True):
    """Get a post and its author by id.

    Checks that the id exists and optionally that the current user is
    the author.

    :param id: id of post to get
    :param check_author: require the current user to be the author
    :return: the post with author information
    :raise 404: if a post with the given id doesn't exist
    :raise 403: if the current user isn't the author
    """
    post = (
        get_db()
        .execute(
            "SELECT p.id, title, body, created, author_id, username"
            " FROM post p JOIN user u ON p.author_id = u.id"
            " WHERE p.id = ?",
            (id,),
        )
        .fetchone()
    )

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post["author_id"] != g.user["id"]:
        abort(403)

    return post

@bp.route('/uploadImage/output.png', methods=['GET', 'POST'])
def parse_request():
    now = datetime.now()
    ts = now.strftime("%Y_%m_%d___%H_%M_%S")
    data = json.loads(request.data)["image"] 
    data =  data.split('base64,')[1]
    im = Image.open(BytesIO(base64.b64decode(data)))
    im.save(basedir + '/images/' + ts +'.png', 'PNG')
    # need posted data here
    # pyautogui.press('enter')
    return Response("{'a':'b'}", status=200, mimetype='application/json')

@bp.route('/uploadImage/live.png', methods=['GET', 'POST'])
def parse_request_live():
    data = json.loads(request.data)["image"] 
    data =  data.split('base64,')[1]
    im = Image.open(BytesIO(base64.b64decode(data)))
    im.save(basedir + '/images/live.png', 'PNG')
    # need posted data here
    request = None
    return Response("{'a':'b'}", status=200, mimetype='application/json')

# @bp.route('/static/manifest.json')
# def send_manafest():
#     return send_from_directory('js', '/static/manifest.json')

@bp.route('/<path:filename>')  
def send_file(filename):  
    return send_from_directory(bp.static_folder, filename)


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    """Create a new post for the current user."""
    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "INSERT INTO post (title, body, author_id) VALUES (?, ?, ?)",
                (title, body, g.user["id"]),
            )
            db.commit()
            return redirect(url_for("blog.index"))

    return render_template("blog/create.html")


@bp.route("/<int:id>/update", methods=("GET", "POST"))
@login_required
def update(id):
    """Update a post if the current user is the author."""
    post = get_post(id)

    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "UPDATE post SET title = ?, body = ? WHERE id = ?", (title, body, id)
            )
            db.commit()
            return redirect(url_for("blog.index"))

    return render_template("blog/update.html", post=post)


@bp.route("/<int:id>/delete", methods=("POST",))
@login_required
def delete(id):
    """Delete a post.

    Ensures that the post exists and that the logged in user is the
    author of the post.
    """
    get_post(id)
    db = get_db()
    db.execute("DELETE FROM post WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for("blog.index"))
