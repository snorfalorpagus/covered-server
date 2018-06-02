import os
from flask import Blueprint, request, abort, current_app, render_template, jsonify
from uuid import uuid4, UUID
import json
from sqlalchemy import and_
from .formatter import create_coverage_table
from .utils import store_upload
from .models import Upload, SourceFile

blueprint = Blueprint("covered", __name__)


def load(uuid):
    if not isinstance(uuid, UUID):  # TODO: not this
        uuid = UUID(uuid.replace("-", ""))
    path = os.path.join(current_app.config["UPLOAD_FOLDER"], f"{uuid.hex}.json")
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
        abort(status=400)
    file = request.files["file"]
    if allowed_file(file.filename):
        filename = f"{uuid.hex}.json"  # TODO: store in database
        path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
        file.save(path)
    with open(path, "r") as f:
        data = json.load(f)
    store_upload(uuid, data)
    # return url to view to the user
    url = f"{request.url_root}view/{uuid}/"
    return url, 200


@blueprint.route("/view/<string:uuid>/")
def index(uuid):
    upload = Upload.query.get(uuid.replace("-", ""))
    content = render_template(
        "view_index.j2",
        uuid=uuid,
        upload=upload,
        source_files=upload.source_files,
    )
    return content


@blueprint.route("/view/<string:uuid>/<path:filename>")
def view(uuid, filename):
    source_file = SourceFile.query.filter(and_(SourceFile.name == filename, Upload.id == uuid.replace("-", ""))).first()

    if not source_file:
        abort(status=404)

    filename = source_file.name
    code = source_file.source
    lookup = {"1": 1, "0": 0, "x": None}
    coverage = [lookup[x] for x in source_file.coverage]

    coverage_table = create_coverage_table(filename, code, coverage)

    content = render_template(
        "coverage.j2",
        uuid=uuid,
        path=filename,
        source_file=source_file,
        coverage_table=coverage_table,
    )

    return content


@blueprint.route("/healthcheck")
def healthcheck():
    # TODO: test database connection
    return jsonify({"status": "OK"}), 200
