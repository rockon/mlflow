import mock

from mlflow.server.handlers import get_endpoints, _create_experiment, _get_request_message
from mlflow.protos.service_pb2 import CreateExperiment


def test_get_endpoints():
    endpoints = get_endpoints()
    create_experiment_endpoint = [e for e in endpoints if e[1] == _create_experiment]
    assert len(create_experiment_endpoint) == 2


def test_can_parse_json():
    request = mock.MagicMock()
    request.method = "POST"
    request.get_json = mock.MagicMock()
    request.get_json.return_value = {"name": "hello"}
    msg = _get_request_message(CreateExperiment(), flask_request=request)
    assert msg.name == "hello"


def test_can_parse_post_json_with_unknown_fields():
    request = mock.MagicMock()
    request.method = "POST"
    request.get_json = mock.MagicMock()
    request.get_json.return_value = {"name": "hello", "WHAT IS THIS FIELD EVEN": "DOING"}
    msg = _get_request_message(CreateExperiment(), flask_request=request)
    assert msg.name == "hello"


def test_can_parse_get_json_with_unknown_fields():
    request = mock.MagicMock()
    request.method = "GET"
    request.query_string = b"name=hello&superDuperUnknown=field"
    msg = _get_request_message(CreateExperiment(), flask_request=request)
    assert msg.name == "hello"


# Previous versions of the client sent a doubly string encoded JSON blob,
# so this test ensures continued compliance with such clients.
def test_can_parse_json_string():
    request = mock.MagicMock()
    request.method = "POST"
    request.get_json = mock.MagicMock()
    request.get_json.return_value = '{"name": "hello2"}'
    msg = _get_request_message(CreateExperiment(), flask_request=request)
    assert msg.name == "hello2"
