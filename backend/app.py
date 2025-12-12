#!/usr/bin/env python3
"""Simple Flask API exposing a stub equation solver."""

from __future__ import annotations

import os
from flask import Flask, jsonify, request
from sympy import *
import re


# make the solution easier to read for the user
# ideally this would be done on the front-end, but for the purposes of this exercise I am doing this on the backend
def pretty_solution(solution):
    # initialize a string to return
    return_string = ""
    # loop through the solution list
    for i in range(0, len(solution)):
        # loop through each inner dictionary and extract the variable and associated value
        for var, val in solution[i].items():
            # concatenate the variable and simplify the associated value and round it if needed
            return_string += str(var) + " = " + str(round(val.evalf(), 4)) + "\n"

    return return_string


# cleans the user input to account for common equation input error
# for example, handles 'x2' and converts it to 'x*2'
# also handles 'x^2' and converts it to 'x**2'
def clean_user_input(equation):
    # initialize all variables
    clean_equation = ""
    previous_value = ""
    has_equals = False
    left_side = ""
    right_side = ""

    # loops through the user input and fix common syntax issues
    for i in range(0, len(equation)):
        # for all char values besides '=', check if the user entered a value like 'x2' or '2x'
        if equation[i] != "=":
            if (equation[i].isnumeric() & previous_value.isalpha()) | (
                    equation[i].isalpha() & previous_value.isnumeric()):
                # if the user entered a value like 'x2' or '2x', then add a '*' between the chars
                # will need to account for cases like 'sinx' in the future
                clean_equation += "*"
            # if the user entered the '^' char, then replace with '**'
            elif equation[i] == "^":
                clean_equation += "*"
                clean_equation += "*"
                previous_value = "*"
                continue
            # add the current char to the clean equation string
            clean_equation += equation[i].strip()
            print(clean_equation)
            # set the previous value string to the current char, for the checks that will run on the next loop
            previous_value = equation[i].strip()
        # if the current char is '='
        else:
            # set the has_equals flag to true
            # need to handle the double equals case
            has_equals = True
            # take the string in the clean_equation variable and set the left side of the equation
            left_side = clean_equation
            # clear the clean_equation and previous_value variables
            clean_equation = ""
            previous_value = ""

    if has_equals:
        right_side = clean_equation

    #other cases that I would add to enhance this parser
    # 1. handle equations that have two or more '=', '+','-', etc
    # 2. handle users passing in strings like 'sinx'

    return clean_equation, has_equals, left_side, right_side


# extracts the expression object from the equation that was passed
def extract_expression(equation):
    # get the clean user input from the clean_user_input_function
    clean_equation, has_equals, left_side, right_side = clean_user_input(equation)

    # if the equation contains an equals sign, then set the right side of the equation
    if has_equals:
        try:
            print(left_side)
            print(right_side)
            # build the full equation using the left and right sides
            expr = Eq(sympify(left_side), sympify(right_side))

        except Exception as e:
            # return an error if the equation building fails
            return None, e

    # if the equation does not contain an equals sign, then use the sympify method to create the expr object
    else:
        try:
            # convert the string into a sympy expression
            expr = sympify(clean_equation)
        except Exception as e:
            return None, e

    return expr, None


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

        # Only allow safe characters
        if not re.match(r'^[0-9a-zA-Z\s\+\-\*/\^\(\)=\.]+$', equation):
            return jsonify({"Invalid characters"}), 400

        #convert the user input into an expr object using extract_expression
        #also retrieve the error if there was any while extracting the expression
        expr, e = extract_expression(equation)

        #if an error was found while extracting the expression, return it
        if expr is None:
            print(f"error type: {type(e)}", flush=True)
            print(f"error message: {e}", flush=True)
            return jsonify({"error": str(e)}), 400

        print("converted to expr")

        #if the expression is just a number, return that number back
        if expr.is_number:
            print("is number")
            return jsonify({"result": str(expr)})

        #if the expression is simple, meaning that it has no variables, we can solve it right away and return
        if expr.free_symbols == set():
            print("is simple expression")
            try:
                #evaluate using the evalf expression
                solution = expr.evalf()
                print("solution found")
                print(str(solution))
                return jsonify({"result": pretty_solution(solution)})
            except Exception as e:
                print(f"error type: {type(e)}", flush=True)
                print(f"error message: {e}", flush=True)
                return jsonify({"error": str(e)}), 400

        # check if we have an algebraic expression
        elif expr.free_symbols != set():
            print("has variables")
            #extract the symbols
            symbol_set = expr.free_symbols
            #convert the symbols to a list
            symbol_list = list(symbol_set)
            try:
                #try to solve the expressionusing the solve method
                solution = solve(expr, symbol_list, dict=True)
                print("solution found")
                print(str(solution))
                #return the result in a user friendly format if successful
                return jsonify({"result": pretty_solution(solution)})
            except Exception as e:
                #return the error if an error is raised
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
