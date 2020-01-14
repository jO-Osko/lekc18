import os
import pytest

from main import app, db

@pytest.fixture
def client():
    app.config["TESTING"] = True
    os.environ["DATABASE_URL"] = "sqlite:///:memory:"
    client = app.test_client()

    db.drop_all()
    db.create_all()

    yield client


def test_no_user(client):
    # Init

    # Do
    response = client.get("/profiles/100")

    # Check
    assert ("UPORABNIK NE OBSTAJA" in str(response.data))
