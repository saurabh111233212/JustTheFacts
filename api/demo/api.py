from flask import Blueprint, jsonify, request, current_app
from flask_cors import CORS
from typing import Tuple
from werkzeug.exceptions import BadRequest


from .get_facts import compare_facts, list_topics, get_facts, get_topic, topics_from_url, update_topic
import random


def create() -> Blueprint:
    """
    This function is called by Skiff to create your application's API. You can
    code to initialize things at startup here.
    """
    api = Blueprint("api", __name__)
    CORS(api, origins=['*'])

    # This tells the machinery that powers Skiff (Kubernetes) that your application
    # is ready to receive traffic. Returning a non 200 response code will prevent the
    # application from receiving live requests.
    @api.route("/")
    def index() -> Tuple[str, int]: # pyright: ignore reportUnusedFunction
        return "", 204

    # The route below is an example API route. You can delete it and add your own.
    @api.route("/api/solve", methods=["POST"])
    def solve(): # pyright: ignore reportUnusedFunction
        data = request.json
        if data is None:
            raise BadRequest("No request body")

        question = data.get("question")
        if question is None or len(question.strip()) == 0:
            raise BadRequest("Please enter a question.")

        choices = data.get("choices", [])
        if len(choices) == 0:
            raise BadRequest("Please enter at least choice value.")

        random.seed()
        selected = random.choice(choices)
        score = random.random()

        # Logs are persisted by 30 days. If you need to persist logs for longer, see:
        # https://skiff.allenai.org/logging.html
        answer = { "answer": selected, "score": score }
        entry = { "message": "Returning Answer", "event": "answer", "answer": answer }
        current_app.logger.info(entry)

        return jsonify(answer)


    # Retrieve facts and other metadata associate with a URL
    @api.route("/api/get-facts", methods=["POST", "GET"])
    def get_facts_route():
        if request.method == 'POST':
            data = request.json
            if data is None:
                raise BadRequest("No request body")
        else:
            data = request.args

        if data is None:
            raise BadRequest("No request body")

        url = data.get("url")
        if url is None or len(url.strip()) == 0:
            raise BadRequest("No url is specified")

        raw_html = data.get("raw_html")
        reset_cache = data.get("reset_cache", False)
        method = data.get("method", "dummy")
        add_embeddings = data.get("add_embeddings", False)

        res = get_facts(url, raw_html=raw_html, reset_cache=reset_cache,
                        method=method, add_embeddings=add_embeddings)
        res = jsonify(res)
        return res

    # Compare facts across sources
    @api.route("/api/compare-facts", methods=["POST", "GET"])
    def compare_facts_route():
        if request.method == 'POST':
            data = request.json
            if data is None:
                raise BadRequest("No request body")
        else:
            data = request.args

        if data is None:
            raise BadRequest("No request body")

        urls = data.get("urls", "")
        topic = data.get("topic")
        if len(urls.strip()) == 0 and topic is None:
            raise BadRequest("Need to specify either urls or topic")
        urls = [x for x in urls.split(",") if x.strip() != ""]
        if len(urls) <= 1 and topic is None:
            raise BadRequest("Specify more than one url, comma-separated")
        method = data.get("method", "dummy")
        allow_multiple_per_source_str = data.get("allow_multiple_per_source", "true")
        allow_multiple_per_source = not (allow_multiple_per_source_str.lower() in ["0", "false"])
        match_threshold_str = data.get("match_threshold", "0.9")
        try:
            match_threshold = float(match_threshold_str)
        except:
            match_threshold = 0.9
        res = compare_facts(urls, topic=topic, method=method, match_threshold=match_threshold,
                            allow_multiple_per_source=allow_multiple_per_source)
        res = jsonify(res)
        return res

    @api.route("/api/get-topic", methods=["POST", "GET"])
    def get_topic_route():
        if request.method == 'POST':
            data = request.json
            if data is None:
                raise BadRequest("No request body")
        else:
            data = request.args

        if data is None:
            raise BadRequest("No request body")

        topic = data.get("topic")
        if topic is None or len(topic.strip()) == 0:
            raise BadRequest("No topic is specified")
        res = get_topic(topic)
        res = jsonify(res)
        return res

    @api.route("/api/update-topic", methods=["POST", "GET"])
    def update_topic_route():
        if request.method == 'POST':
            data = request.json
            if data is None:
                raise BadRequest("No request body")
        else:
            data = request.args

        if data is None:
            raise BadRequest("No request body")

        topic = data.get("topic")
        if topic is None or len(topic.strip()) == 0:
            raise BadRequest("No topic is specified")
        urls = data.get("urls")
        if urls is None:
            raise BadRequest("No urls is specified")
        urls = [x for x in urls.split(",") if x.strip() != ""]

        res = update_topic(topic, urls)
        res = jsonify(res)
        return res


    @api.route("/api/list-topics", methods=["POST", "GET"])
    def list_topics_route():
        return jsonify(list_topics())

    @api.route("/api/topics-from-url", methods=["POST", "GET"])
    def topics_from_url_route():
        if request.method == 'POST':
            data = request.json
            if data is None:
                raise BadRequest("No request body")
        else:
            data = request.args

        if data is None:
            raise BadRequest("No request body")

        url = data.get("url")
        if url is None or len(url.strip()) == 0:
            raise BadRequest("No url is specified")

        return jsonify(topics_from_url(url))


    # @api.route("/api/get-facts2", methods=['POST'])
    # def get_facts():
    #     data = request.json
    #     return jsonify({
    #         'facts': [
    #             'The U.S. Supreme Court has reinstated a regulation aimed at controlling the spread of ghost guns, or firearms with no serial numbers.',
    #             'A federal judge from Texas previously invalidated this regulation but it is now back in effect as the Biden administration appeals.',
    #             'The 5-4 decision by the Supreme Court to suspend the Texas judge\'s ruling saw the concurrence of Chief Justice John Roberts and Justice Amy Coney Barrett with three liberal justices.',
    #             'Four of the Supreme Court justices, namely Samuel Alito, Neil Gorsuch, Brett Kavanaugh, and Clarence Thomas, opposed the interim reinstatement of the regulation.',
    #             'In 2021, over 19,000 ghost guns were confiscated at crime scenes by local law enforcement agencies, suggesting a sharp increase from the numbers recorded five years prior.',
    #         ]
    #     })

    return api
