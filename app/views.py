import os
from flask import Blueprint, request, abort, current_app, render_template, jsonify
from werkzeug.utils import secure_filename
from uuid import uuid4, UUID
import json
from .formatter import create_coverage_table

blueprint = Blueprint("covered", __name__)


def load(uuid):
    if not isinstance(uuid, UUID):  # TODO: not this
        uuid = UUID(uuid)
    path = os.path.join(current_app.config["UPLOAD_FOLDER"], f"{uuid.hex}.json")
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
    if allowed_file(file.filename):
        filename = f"{uuid.hex}.json"  # TODO: store in database
        file.save(os.path.join(current_app.config["UPLOAD_FOLDER"], filename))
    # return url to view to the user
    url = f"{request.url_root}view/{uuid}/"
    return url, 200


@blueprint.route("/view/<string:uuid>/")
def index(uuid):
    uuid = uuid.replace("-", "")
    data = load(uuid)
    content = render_template(
        "view_index.j2",
        source_files=data["source_files"],
        summary=data["summary"],
        git=data["git"],
    )
    return content


@blueprint.route("/view/<string:uuid>/<path:filename>")
def view(uuid, filename):
    data = load(uuid)

    index = {source_file["name"]: n for n, source_file in enumerate(data["source_files"])}

    idx = index[filename]

    source_file = data["source_files"][idx]
    filename = source_file["name"]
    code = source_file["source"]
    coverage = source_file["coverage"]

    coverage_table = create_coverage_table(filename, code, coverage)

    return render_template("coverage.j2", path=filename, coverage_table=coverage_table, summary=source_file["summary"])


@blueprint.route("/healthcheck")
def healthcheck():
    # TODO: test database connection
    return jsonify({"status": "OK"}), 200
