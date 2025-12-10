#!/usr/bin/env python3
"""Simple Flask API exposing a stub equation solver."""

from __future__ import annotations

import os
from flask import Flask, jsonify, request
from sympy import *


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

        #convert the string into a sympy expression
        expr = sympify(equation)

        #if the expression is simple, meaning that it has no variables, we can solve it right away and return
        if expr.expr_free_symbols == set():
            solution = expr.evalf()
            return jsonify({"result": str(solution)})

        # Parse the equation string the user sent and check if there are any variables in the expression
        # check if its a differential equation
        # check if its a polynomial equation
        # check if its a Diophantine Equation

        #if the expression is simple and doesn't involve variables that we need to solve for (i.e. 2*2)
        expr.evalf() #we can return this value

        #if there are variables that we need to solve for, and it's an algebric expression
        solve(x**4 - 256, x, dict=True)

        # if its a differential equation

        # if its a polynomial equation

        # if its a Diophantine Equation


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
