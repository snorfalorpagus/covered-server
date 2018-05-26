import os
from flask import Blueprint, request, abort, current_app, render_template
from werkzeug.utils import secure_filename
from uuid import uuid4, UUID
import json
from .formatter import run

blueprint = Blueprint("covered", __name__)


def load(uuid):
    if not isinstance(uuid, UUID):  # TODO: not this
        uuid = UUID(uuid)
    path = f"/tmp/covered/{uuid.hex}.json" # TODO
    print(path)
    with open(path, "r") as f:
        data = json.load(f)
    return data


@blueprint.route("/")
def hello():
    return "Hello, World\n"


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {"gz", "json"}


@blueprint.route("/upload", methods=["POST"])
def upload():
    uuid = uuid4()
    # store the data
    if "file" not in request.files:
        abort()
    file = request.files["file"]
    print("ok", file.filename)
    if allowed_file(file.filename):
        print("OK")
        # filename = secure_filename(file.filename)
        filename = f"/tmp/covered/{uuid.hex}.json"  # TODO: store in database
        file.save(os.path.join(current_app.config["UPLOAD_FOLDER"], filename))
    # return url to view to the user
    url = f"{request.url_root}view/{uuid}/"
    return url, 200


@blueprint.route("/view/<string:uuid>/")
def index(uuid):
    uuid = uuid.replace("-", "")
    data = load(uuid)
    return render_template("view_index.j2", source_files=data["source_files"])


@blueprint.route("/view/<string:uuid>/<path:filename>")
def view(uuid, filename):
    data = load(uuid)

    index = {source_file["name"]: n for n, source_file in enumerate(data["source_files"])}

    idx = index[filename]

    source_file = data["source_files"][idx]
    filename = source_file["name"]
    code = source_file["source"]
    coverage = source_file["coverage"]

    output = run(filename, code, coverage)
    
    return output
