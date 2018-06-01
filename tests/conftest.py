import pytest

from app import create_app

@pytest.fixture
def app():
    _app = create_app()
    with _app.app_context():
        yield _app


@pytest.fixture
def client(app):
    return app.test_client()
