#!/usr/bin/env python3
"""Simple Flask API exposing a stub equation solver."""

from __future__ import annotations

import os
from flask import Flask, jsonify, request


def create_app() -> Flask:
    app = Flask(__name__)

    @app.after_request
    def add_cors_headers(response):  # type: ignore[override]
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        return response

    @app.get("/solve")
    def solve():
        equation = (request.args.get("equation") or "").strip()
        if not equation:
            return jsonify({"error": "Missing 'equation' query parameter"}), 400

        #A few things to think about:

        #What if the user sends an invalid equation?
        #What if the equation has no solution?
        #What if there are multiple solutions?
        #How should you format the result?

        #Parse the equation string the user sent

        #Use sympy to solve it

        #Format the solution(s)

        #Return them in the JSON response


        return jsonify({"result": f"not implemented: solving '{equation}'"})



    @app.route("/", methods=["GET"])
    def root():
        return jsonify({"message": "Equation API. Try /solve?equation=1+1"})

    return app


def run() -> None:
    port = int(os.environ.get("PORT", 8000))
    app = create_app()
    app.run(host="0.0.0.0", port=port, debug=False)


if __name__ == "__main__":
    run()
