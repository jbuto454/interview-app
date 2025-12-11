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
    def solve_equation():
        equation = (request.args.get("equation") or "").strip()
        print(str(equation), flush=True)
        if not equation:
            return jsonify({"error": "Missing 'equation' query parameter"}), 400

        #A few things to think about:
        #What if the user sends an invalid equation?
        #What if the equation has no solution?
        #What if there are multiple solutions?
        #How should you format the result?
        clean_equation = ""
        previous_value = ""
        has_equals = False
        left_side = ""
        right_side = ""

        for i in range(0, len(equation)):
            if equation[i] != "=":
                if (equation[i].isnumeric() & previous_value.isalpha()) | (equation[i].isalpha() & previous_value.isnumeric()):
                    clean_equation += "*"
                elif equation[i] == "^":
                    clean_equation += "*"
                    clean_equation += "*"
                    previous_value = equation[i].strip()
                    continue
                clean_equation += equation[i].strip()
                print(clean_equation)
                previous_value = equation[i].strip()
            else:
                has_equals = True
                left_side = clean_equation
                clean_equation = ""

        if has_equals:
            right_side = clean_equation
            try:
                print(left_side)
                print(right_side)
                expr = Eq(sympify(left_side), sympify(right_side))
            except Exception as e:
                print(f"error type: {type(e)}", flush=True)
                print(f"error message: {e}", flush=True)
                return jsonify({"error": str(e)}), 400

        else:
            try:
                #convert the string into a sympy expression
                expr = sympify(clean_equation)
            except Exception as e:
                print(f"error type: {type(e)}", flush=True)
                print(f"error message: {e}", flush=True)
                return jsonify({"error": str(e)}), 400

        print("converted to expr")

        if expr is None:
            return jsonify({"error": "Invalid 'equation' query parameter"}), 400

        #if the expression is just a number, return that number back
        if expr.is_number:
            print("is number")
            return jsonify({"result": str(expr)})

        #if the expression is simple, meaning that it has no variables, we can solve it right away and return
        if expr.free_symbols == set():
            print("is simple expression")
            try:
                solution = expr.evalf()
                print("solution found")
                print(str(solution))
                return jsonify({"result": str(solution)})
            except Exception as e:
                print(f"error type: {type(e)}", flush=True)
                print(f"error message: {e}", flush=True)
                return jsonify({"error": str(e)}), 400

        # check if we have an algebraic expression
        elif expr.free_symbols != set():
            print("has variables")
            symbol_set = expr.free_symbols
            symbol_list = list(symbol_set)
            try:
                solution = solve(expr, symbol_list, dict=True)
                print("solution found")
                print(str(solution))

                return jsonify({"result": str(solution)})
            except Exception as e:
                print(f"error type: {type(e)}", flush=True)
                print(f"error message: {e}", flush=True)
                return jsonify({"error": str(e)}), 400

        else:
            return jsonify({"error": "Invalid 'equation' query parameter"}), 400


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
