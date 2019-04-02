from schema import SchemaError
from flask import request, jsonify

from app import app
from crawlers.controller import get_trending_threads_on_subreddits
from crawlers.views.view_handler import REQUEST_TRENDING_THREADS_FORM_SCHEMA


@app.route('/subreddits_trending_threads', methods=["GET"])
def request_trending_threads_on_subreddits():
    """
    This function receives and processes a GET request for the trending threads of a given list of sub_reddits
    :return: a message
    """
    app_json = request.get_json()
    try:
        REQUEST_TRENDING_THREADS_FORM_SCHEMA.validate(app_json)
    except SchemaError as err:
        return jsonify({"error": str(err)})
    subreddits = app_json.get('subreddits').split(';')
    subreddits_trending_threads = get_trending_threads_on_subreddits(subreddits=subreddits)
    return jsonify(subreddits_trending_threads)
