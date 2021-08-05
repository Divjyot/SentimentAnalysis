from json import dumps as jsondump
from http import HTTPStatus
from flask import Blueprint, jsonify, request
from werkzeug.exceptions import BadRequest
from transformers import pipeline
from ..services.model_inference import SentimentPredictor, SentimentPredictorResponse
from ..exceptions.exceptions import QueryEmptyNoneValueError, QueryTypeError
from flask import current_app as app
import logging
from enums import API_CONFIG

logger = logging.getLogger(__name__)
sentiment_analysis = Blueprint("sentiment_analysis", __name__)
predictor = SentimentPredictor(pipeline("sentiment-analysis"))


# Prediction route
@sentiment_analysis.route("/predict", methods=["POST"])
def predict():
    """API Route that enables predictions for sentiment-analysis

    Raises:
        QueryEmptyNoneValueError: if `query` is empty or none
        BadRequest: if `query` key or whole body is missing
        Exception: if unkwown exception arrises, logs in background.
    Returns:
        json/dict: with keys `score` and `label`
    """
    if request.method == "POST":
        headers = dict(request.headers)
        print(headers)
        if app.config[API_CONFIG.SECRET_KEY.value] == headers.get("Secret-Key", None):
            try:
                if (req_body := request.get_json(force=True)) is not None:
                    if (query := req_body.get("query", None)) is not None:
                        response: SentimentPredictorResponse = jsonify(predictor.get_prediction(query))
                        status_code = HTTPStatus.OK.value
                    else:
                        raise QueryEmptyNoneValueError("Request json-body is missing the required `query` key.")
                else:
                    raise BadRequest()
            except (QueryEmptyNoneValueError, QueryTypeError) as e:
                response = str(e)
                status_code = HTTPStatus.BAD_REQUEST.value
            except BadRequest:
                response = (
                    "API is unable to parse request body. A json with `query` as key and `text` as value is required."
                )
                status_code = HTTPStatus.BAD_REQUEST.value
            except Exception as e:
                response = "An error has occured at server"
                status_code = HTTPStatus.INTERNAL_SERVER_ERROR.value
                logger.exception(str(e), stack_info=True)
        else:
            response, status_code = "Unauthorised", HTTPStatus.UNAUTHORIZED.value
        return response, status_code
