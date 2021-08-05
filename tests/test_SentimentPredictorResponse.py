import pytest
from app.services.model_inference import SentimentPredictorResponse


@pytest.fixture
def label_positive():
    return "POSITIVE"


@pytest.fixture
def label_negative():
    return "NEGATIVE"


@pytest.fixture
def score_float():
    return 0.983649492263794


@pytest.fixture
def score_int():
    return 98


@pytest.fixture
def negative_SentimentPredictorResponse(label_negative, score_float):
    return SentimentPredictorResponse(label_negative, score_float)


@pytest.fixture
def positive_SentimentPredictorResponse(label_positive, score_float):
    return SentimentPredictorResponse(label_positive, score_float)


# TESTS


@pytest.mark.parametrize(
    "a_SentimentPredictorResponse,a_label",
    [
        (
            pytest.lazy_fixture("positive_SentimentPredictorResponse"),
            pytest.lazy_fixture("label_positive"),
        ),
        (
            pytest.lazy_fixture("negative_SentimentPredictorResponse"),
            pytest.lazy_fixture("label_negative"),
        ),
    ],
)
def test_label_SentimentPredictorResponse(a_SentimentPredictorResponse, a_label):
    assert a_SentimentPredictorResponse.label == a_label


def test_score_rounded_SentimentPredictorResponse(positive_SentimentPredictorResponse, score_float):
    assert positive_SentimentPredictorResponse.score == round(score_float * 100.0, None)
