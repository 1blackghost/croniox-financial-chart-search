'''
This script contains the views/routes of the website

'''

from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import json
from api_utils import caller


app = Flask(__name__)
CORS(app)

@app.route("/search", methods=["POST"])
def search():
    '''
        /search url entry point.

        Args:
            None
        Returns:
            jsonified data
        Raises:
            None
            
    '''

    finder = request.json["name"]
    data = caller.fetch_data(finder)
    print(data)
    return jsonify(data)


@app.route("/curve_fitting", methods=["POST"])
def curve_fitting():
    '''
        /curve_fitting url entry point.

        Args:
            None
        Returns:
            jsonified data
        Raises:
            ArrayIndexOutOfBoundError
            
    '''

    data = request.json["data"]
    degree = request.json.get("degree", 3)

    equation = caller.get_eq(data,degree)

    return jsonify({"equation": equation})

if __name__ == "__main__":
    app.run(debug=True)
