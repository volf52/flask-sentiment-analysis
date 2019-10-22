import os

import requests
import sentry_sdk
from bs4 import BeautifulSoup
from flask import Flask, flash, redirect, render_template, request, url_for
from sentry_sdk.integrations.flask import FlaskIntegration
from textblob import TextBlob

from .sentiment import PageSentiment

sentry_sdk.init(
    dsn="https://2555ba93fc344634bb545965fb8f44e4@sentry.io/1792065",
    integrations=[FlaskIntegration()],
)


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.update(SECRET_KEY="secretkey")

    try:
        os.makedirs(app.instance_path)
    except OSError as e:
        pass

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/results", methods=("POST",))
    def results():
        url = request.form.get("url")
        try:
            response = requests.get(url)
            if response.status_code != 200:
                raise RuntimeError()
        except:
            # give error - invalid url
            flash("Invalid url. Please fix and resubmit")
            return redirect(url_for("index"))

        # parse results
        soup = BeautifulSoup(response.content, "html.parser")
        if soup.find("h1"):
            header = soup.find("h1").get_text()
        else:
            header = soup.title.get_text()

        # create TextBlob instance
        blob = TextBlob(soup.get_text())

        # process TextBlob text analytics results
        page_results = PageSentiment(url, header, blob)

        return render_template("results.html", page_results=page_results)

    return app
