from flask import (
    Flask,
    redirect,
    url_for,
    request,
    render_template,
    jsonify,
    make_response,
)
from pymongo import MongoClient
import json

app = Flask(__name__)

mclient = MongoClient("mongodb", 27017)
db = mclient.demo
collection = db["mycol"]


def get_prediction(db_data):
    # function to get a prediction from the database
    # based on probability value
    prediction = {}
    best_prediction = {}
    len_response = len(db_data["output"])
    if len_response > 1:
        max_prob_index = 0
        max_prob_val = db_data["output"][0]["probability"]
        for i in range(1, len_response):
            cur_prob_val = db_data["output"][i]["probability"]
            if cur_prob_val > max_prob_val:
                max_prob_val = cur_prob_val
                max_prob_index = i

        prediction = {"imageId": db_data["imageId"], "probability": db_data["output"][max_prob_index]["probability"],
                      "label": db_data["output"][max_prob_index]["label"],
                      "result": db_data["output"][max_prob_index]["result"]}

        best_prediction["prediction"] = prediction
        print("best_prediction ", prediction)
        # weak_prediction = get_weak_prediction(response)
        # prediction["bestPrediction"] = best_prediction
        # prediction["weakPrediction"] = weak_prediction

    else:
        #prediction["imageId"] = db_data["imageId"]
        #prediction["probability"] = db_data["output"][0]["probability"]
        #prediction["label"] = db_data["output"][0]["label"]
        #prediction["result"] = db_data["output"][0]["result"]

        prediction = {
            "imageId": db_data["imageId"],
            "probability": db_data["output"][0]["probability"],
            "label": db_data["output"][0]["label"],
            "result": db_data["output"][0]["result"],
        }
        best_prediction["prediction"] = prediction
    return best_prediction


def get_weak_prediction(db_data):
    # function to get all the weak predictions for an image id

    len_res = len(db_data["output"])
    weak_predictions = {}
    pred = []
    if len_res > 1:
        for i in range(len_res):
            if db_data["output"][i]["probability"] < 0.7:
                pred.append(
                    {
                        "probability": db_data["output"][i]["probability"],
                        "label": db_data["output"][i]["label"],
                        "result": db_data["output"][i]["result"],
                    }
                )
        weak_predictions["pred_less_than_0.7"] = pred
        print("weak predictions: ", weak_predictions)
    return weak_predictions


# rest api to get all image related data
@app.route("/get/prediction/v1.0/imageid", methods=["GET"])
def get_all_predictions():
    # rest api to get all image related data

    output = []
    for rows in collection.find():
        # len_output = len(rows["output"])
        # print(len_output, flush=True)
        output.append({"imageId": rows["imageId"], "output": rows["output"]})

    return jsonify({"result": output})


@app.route("/get/prediction/v1.0/imageid/<string:imageid>", methods=["GET"])
def get_prediction(imageid):
    # rest api to get data for a particular imageid
    db_values = collection.find_one({"imageId": imageid})

    if db_values:
        output_prediction = get_prediction(db_values)
        weak_predictions = get_weak_prediction(db_values)
        print(output_prediction, flush=True)
        return jsonify({"result": output_prediction, "weak_predictions": weak_predictions})
    else:
        output_prediction = "No results found"
        weak_predictions = "None available"
        return jsonify({"result": output_prediction, "weak_predictions": weak_predictions})


@app.errorhandler(404)
def not_found(error):
    # error handling for all the other endpoints
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
