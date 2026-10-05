"""
app.py
======
Flask server for the Big 12 linear-system ranking demo.

    GET /               -> the main page
    GET /api/rankings   -> JSON with rankings, the matrix C, vector b, and games
"""

from flask import Flask, jsonify, render_template

from lin_eqt import compute_rankings

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/rankings")
def api_rankings():
    return jsonify(compute_rankings())


if __name__ == "__main__":
    app.run(debug=True)
