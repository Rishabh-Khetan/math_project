"""
app.py
======
Flask server for the Big 12 linear-system ranking demo.

    GET /               -> the main page (public/index.html)
    GET /api/rankings   -> JSON with rankings, the matrix C, vector b, and games

The page, CSS and JS are plain static files in public/. On Vercel the CDN
serves them directly (public/index.html -> /, public/style.css -> /style.css),
so Flask only has to handle the API. Pointing Flask at the same folder makes
`python app.py` behave identically when running locally.
"""

from flask import Flask, jsonify

from lin_eqt import compute_rankings

app = Flask(__name__, static_folder="public", static_url_path="")


@app.route("/")
def index():
    # Used locally; on Vercel the CDN answers "/" with public/index.html.
    return app.send_static_file("index.html")


@app.route("/api/rankings")
def api_rankings():
    return jsonify(compute_rankings())


if __name__ == "__main__":
    app.run(debug=True)
