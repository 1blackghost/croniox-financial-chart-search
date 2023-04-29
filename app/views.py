'''
This script contains the views/routes of the website

'''

from flask import jsonify,request,session
from api_utils import caller
from main import app



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
    function = request.json["func"]
    data = caller.fetch_data(finder,function)
    if data["status"]=="bad":
        return jsonify(data)
    else:
        session["data"]=data
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

    if "data" in session:
        data=session["data"]
        print(data)
        new=data

    else:
        print("return error block")
    degree = request.json.get("degree", 3)

    equation = caller.get_eq(new,degree)

    return jsonify({"equation": equation})
