import pytest
from transformers.pipelines.base import Pipeline
from app.services.model_inference import SentimentPredictor
from tests.test_SentimentPredictorResponse import (
    label_positive,
    label_negative,
    score_float,
    score_int,
    negative_SentimentPredictorResponse,
    positive_SentimentPredictorResponse,
)
from app.exceptions.exceptions import QueryEmptyNoneValueError, QueryTypeError
import dataclasses


class MockPipeline(Pipeline):
    def __init__(self, label, score, predict_type="valid") -> None:
        self.label = label
        self.score = score
        self.predict_type = predict_type

    def __call__(self, query, *args, **kwargs):
        method_to_call = getattr(self, f"predict_{self.predict_type}")
        return method_to_call()

    def predict_valid(self):
        return [{"label": self.label, "score": self.score}]

    # empty
    def predict_empty(self):
        return []

    def predict_empty_sub_dict(self):
        return [{}]

    def predict_none(self):
        return None

    # missing
    def predict_missing_label(self):
        return [{"score": self.score}]

    def predict_missing_score(self):
        return [{"label": self.label}]

    # unkwown keys
    def predict_unknown_key(self):
        return [{"label": self.label, "score": self.score, "unknown_key1": "unknown_value1"}]

    def predict_all_unkown_keys(self):
        return [{"unknown_key1": "unknown_value1", "unknown_key2": "unknown_value2"}]


# Mocked Model Objects
@pytest.fixture
def mock_model__positive(label_positive, score_float):
    return MockPipeline(label_positive, score_float)


@pytest.fixture
def mock_model__empty(label_positive, score_float):
    return MockPipeline(label_positive, score_float, predict_type="empty")


@pytest.fixture
def mock_model__empty_sub_dict(label_positive, score_float):
    return MockPipeline(label_positive, score_float, predict_type="empty_sub_dict")


@pytest.fixture
def mock_model__none(label_positive, score_float):
    return MockPipeline(label_positive, score_float, predict_type="none")


@pytest.fixture
def mock_model__missing_label(label_positive, score_float):
    return MockPipeline(label_positive, score_float, predict_type="missing_label")


@pytest.fixture
def mock_model__missing_score(label_positive, score_float):
    return MockPipeline(label_positive, score_float, predict_type="missing_score")


@pytest.fixture
def mock_model__unknown_key(label_positive, score_float):
    return MockPipeline(label_positive, score_float, predict_type="unknown_key")


@pytest.fixture
def mock_model__all_unkown_keys(label_positive, score_float):
    return MockPipeline(label_positive, score_float, predict_type="all_unkown_keys")


# Sentiment Predictor Objects
@pytest.fixture
def positive_SentimentPredictor(mock_model__positive):
    return SentimentPredictor(mock_model__positive)


@pytest.fixture
def empty_SentimentPredictor(mock_model__positive):
    return SentimentPredictor(mock_model__positive)


def test_positive_SentimentPredictor(positive_SentimentPredictor, positive_SentimentPredictorResponse):
    predictions = positive_SentimentPredictor.get_prediction("This is sample string not under test")
    assert predictions == dataclasses.asdict(positive_SentimentPredictorResponse)


def test_positive_score_SentimentPredictor(positive_SentimentPredictor, score_int):
    predictions = positive_SentimentPredictor.get_prediction("This is sample string not under test")
    assert predictions.get("score") == score_int


def test_positive_against_negative_SentimentPredictor(
    positive_SentimentPredictor,
    negative_SentimentPredictorResponse,
):
    predictions = positive_SentimentPredictor.get_prediction("This is sample string not under test")
    assert predictions != negative_SentimentPredictorResponse


### UNWANTED
def test_against_unexpected_query_SentimentPredictor(positive_SentimentPredictor):
    with pytest.raises(QueryEmptyNoneValueError):
        positive_SentimentPredictor.get_prediction("")

    with pytest.raises(QueryEmptyNoneValueError):
        positive_SentimentPredictor.get_prediction(None)

    with pytest.raises(QueryTypeError):
        positive_SentimentPredictor.get_prediction(0.1234)


def test_unexpected_predictions_SentimentPredictor(
    mock_model__positive,
    mock_model__empty,
    mock_model__empty_sub_dict,
    mock_model__none,
    mock_model__missing_label,
    mock_model__missing_score,
    mock_model__unknown_key,
    mock_model__all_unkown_keys,
):
    _sample_str = "This is sample string not under test"

    assert SentimentPredictor(mock_model__empty).get_prediction(_sample_str) == None

    assert SentimentPredictor(mock_model__none).get_prediction(_sample_str) == None

    with pytest.raises(QueryTypeError):
        SentimentPredictor(mock_model__positive).get_prediction(0.1234)

    with pytest.raises(TypeError):
        SentimentPredictor(mock_model__empty_sub_dict).get_prediction(_sample_str)

    with pytest.raises(TypeError):
        SentimentPredictor(mock_model__missing_label).get_prediction(_sample_str)

    with pytest.raises(TypeError):
        SentimentPredictor(mock_model__missing_score).get_prediction(_sample_str)

    with pytest.raises(TypeError):
        SentimentPredictor(mock_model__unknown_key).get_prediction(_sample_str)

    with pytest.raises(TypeError):
        SentimentPredictor(mock_model__all_unkown_keys).get_prediction(_sample_str)
