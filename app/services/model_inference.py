import dataclasses
from transformers.pipelines import Pipeline
from ..exceptions.exceptions import QueryEmptyNoneValueError, QueryTypeError

@dataclasses.dataclass()
class SentimentPredictorResponse:
    """Class for keeping track of Sentiment Predictor's response."""

    label: str
    score: float

    def __init__(self, label, score) -> None:
        """Initialises data class for Sentiment Analysis's repsonse

        Args:
            label (str): [description]
            score (float): [description]
        """
        self.label = label
        assert score <= 1.0
        self.score = round(score * 100.0)


class SentimentPredictor:
    """A class to facilitate sentiment anaylsis predictions."""

    def __init__(self, model) -> None:
        assert isinstance(model, Pipeline)
        self.model: Pipeline = model

    def get_prediction(self, query: str) -> dict:
        """Allows to get predictions from sentiment analysis model.

        Args:
            query (str): desired string to perform the sentiment analysis upon.

        Raises:
            QueryEmptyNoneValueError: if `query` is empty or `none`
            QueryTypeError: if `query` is of type other than `str`

        Returns:
            dict: with keys `score` and `label` denoting outputs from model,
            where `score` is rounded to nearest integer value.

            None: if model's prediction is None object or a size of list not 1.
        """
        if (query is None) or (query == ""):
            raise QueryEmptyNoneValueError(query)

        if not isinstance(query, str):
            raise QueryTypeError(query)

        if (predictions := self.model(query)) is not None:
            predictions = list(map(lambda s: SentimentPredictorResponse(**s), predictions))
            if len(predictions) == 1:
                return dataclasses.asdict(predictions[0])
