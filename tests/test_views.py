import pytest
import os

TEST_FOLDER = os.path.dirname(__file__)
TEST_DATA_FOLDER = os.path.join(TEST_FOLDER, "test_data")


def test_hello(client):
    res = client.get("/")
    assert res.status_code == 200


def test_healthcheck(client):
    res = client.get("/healthcheck")
    assert res.status_code == 200


def test_upload_empty(client):
    res = client.post("/upload")
    assert res.status_code == 400


def test_upload(client):
    # upload some sample data
    with open(os.path.join(TEST_DATA_FOLDER, "6c4a71546b9941a2a324d07910488f7d.json"), "rb") as f:
        res = client.post("/upload", data=dict(file=(f, 'test.json'),))
    assert res.status_code == 200
    # access the coverage report
    url = res.get_data(as_text=True)
    assert url.startswith("http")
    res = client.get(url)
    assert res.status_code == 200
    text = res.get_data(as_text=True)
    # search the response for the git hash from the upload
    assert "c5752deb2a410f028c2c39b291351928646fca51" in text
    # get coverge report for one of the files
    res = client.get(url + "hello.py")
    assert res.status_code == 200
    # get coverge report for empty file
    res = client.get(url + "empty.py")
    assert res.status_code == 200
    # get coverge report for missing file
    res = client.get(url + "notfound.py")
    assert res.status_code == 404
