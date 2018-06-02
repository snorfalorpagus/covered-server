from .models import db, Upload, SourceFile


COVERAGE_DATA = {
    0: "0",
    1: "1",
    None: "x",
}


def store_upload(uuid, data):
    upload = Upload()
    upload.id = uuid.hex
    upload.hit = data["summary"]["hit"]
    upload.missing = data["summary"]["missing"]
    upload.excluded = data["summary"]["excluded"]
    upload.total = data["summary"]["total"]
    upload.coverage_percent = data["summary"]["coverage"]
    upload.git_branch = data["git"]["branch"]
    upload.git_commit = data["git"]["commit"]
    for source_file_data in data["source_files"]:
        source_file = store_file(source_file_data)
        upload.source_files.append(source_file)
        db.session.add(source_file)
    db.session.add(upload)
    db.session.commit()
    return upload.id


def store_file(data):
    source_file = SourceFile()
    source_file.name = data["name"]
    source_file.source = data["source"]
    source_file.coverage = "".join((COVERAGE_DATA[x] for x in data["coverage"]))
    source_file.hit = data["summary"]["hit"]
    source_file.missing = data["summary"]["missing"]
    source_file.excluded = data["summary"]["excluded"]
    source_file.total = data["summary"]["total"]
    source_file.coverage_percent = data["summary"]["coverage"]
    return source_file


def load(id):
    upload = Upload.query.get(id)
    return upload
