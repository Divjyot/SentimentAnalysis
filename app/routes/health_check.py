from flask import Blueprint
import os

health_check = Blueprint("health_check", __name__)

# Test API up
@health_check.route("/", methods=["GET"])
def check_api():
    """Test route to check if service is up and running

    Returns:
        str: message to indicate service status
    """
    return "Sentiment Analysis API is up & running!"
