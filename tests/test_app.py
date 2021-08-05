import pytest
from app import create_app


@pytest.fixture
def request_header_secret():
    return "dev"


@pytest.fixture
def request_body_positive():
    return {"query": "I am having a great day!"}


@pytest.fixture
def request_body_negative():
    return {"query": "I am feeling sad today"}


@pytest.fixture
def http_error_METHOD_NOT_ALLOWED():
    return 405


@pytest.fixture
def http_error_BAD_REQUEST():
    return 400


@pytest.fixture
def http_OK():
    return 200


@pytest.fixture
def flask_client():
    app = create_app()
    with app.test_client() as client:
        yield client


## TESTS
#########

# Index/ Health Check Test
def test_health_check(flask_client):
    res = flask_client.get("/")
    assert b"up & running" in res.data


## OK REQUESTS Tests
####################


def test_predict_positive(flask_client, http_OK, request_body_positive, request_header_secret):
    res = flask_client.post("/predict", json=request_body_positive, headers={"Secret-Key": request_header_secret})
    assert res.status_code == http_OK
    assert b"POSITIVE" in res.data


def test_predict_negative(flask_client, http_OK, request_body_negative, request_header_secret):
    res = flask_client.post("/predict", json=request_body_negative, headers={"Secret-Key": request_header_secret})
    assert res.status_code == http_OK
    assert b"NEGATIVE" in res.data


## BAD REQUESTS Tests
####################


def test_GET_instead_POST(flask_client, http_error_METHOD_NOT_ALLOWED, request_header_secret):
    res = flask_client.get("/predict", json={"query": ""}, headers={"Secret-Key": request_header_secret})
    assert res.status_code == http_error_METHOD_NOT_ALLOWED


## Body


def test_None_body(flask_client, http_error_BAD_REQUEST, request_header_secret):
    res = flask_client.post("/predict", json=None, headers={"Secret-Key": request_header_secret})
    assert res.status_code == http_error_BAD_REQUEST


def test_empty_body(flask_client, http_error_BAD_REQUEST, request_header_secret):
    res = flask_client.post("/predict", json={}, headers={"Secret-Key": request_header_secret})
    assert res.status_code == http_error_BAD_REQUEST


## Query


def test_none_query(flask_client, http_error_BAD_REQUEST, request_header_secret):
    res = flask_client.post("/predict", json={"query": None}, headers={"Secret-Key": request_header_secret})
    assert res.status_code == http_error_BAD_REQUEST


def test_empty_query(flask_client, http_error_BAD_REQUEST, request_header_secret):
    res = flask_client.post("/predict", json={"query": ""}, headers={"Secret-Key": request_header_secret})
    assert res.status_code == http_error_BAD_REQUEST


def test_non_string_numerical(flask_client, http_error_BAD_REQUEST, request_header_secret):
    res = flask_client.post("/predict", json={"query": 456123}, headers={"Secret-Key": request_header_secret})
    assert res.status_code == http_error_BAD_REQUEST


def test_non_string_object(flask_client, http_error_BAD_REQUEST, request_header_secret):
    res = flask_client.post("/predict", json={"query": ["I am happy"]}, headers={"Secret-Key": request_header_secret})
    assert res.status_code == http_error_BAD_REQUEST
