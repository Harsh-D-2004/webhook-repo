from flask import Blueprint, json, request, jsonify, current_app
from app.webhook.controller import extract_github_request
from app.extensions import mongo
from bson import json_util

webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')

# webhook route for receiving github webhook events
@webhook.route('/receiver', methods=["POST"])
def receiver():

    github_request = extract_github_request(request.json)

    if github_request:
        try:
            
            assert mongo.db is not None
            collection = mongo.db["github-actions"]

            result = collection.insert_one(github_request.to_dict())

            print(f"Document inserted successfully with ID: {result.inserted_id}")

            return jsonify({
                "status": "success",
                "message": "Webhook processed successfully",
                "data": github_request.to_dict(),
                "inserted_id": str(result.inserted_id)
            }), 200

        except Exception as e:
            print(f"Error inserting document to MongoDB: {str(e)}")
            return jsonify({
                "status": "error",
                "message": f"Failed to save to database: {str(e)}"
            }), 500

    else:
        print("Webhook event type not supported - ignoring")
        return jsonify({
            "status": "ignored",
            "message": "Webhook event type not supported"
        }), 200

# webhook route for fetching latest data from mongodb
@webhook.route('/data', methods=["GET"])
def get_latest_data():

    try:
        assert mongo.db is not None
        collection = mongo.db["github-actions"]

        data_raw = collection.find().sort("timestamp", -1).limit(10)
        data = list(data_raw)

        print(f"Retrieved {len(data)} documents from github-actions collection")

        serialized_data = json.loads(json_util.dumps(data))

        return jsonify({
            "status": "success",
            "message": f"Retrieved {len(data)} latest documents",
            "data": serialized_data
        }), 200

    except Exception as e:
        print(f"Error fetching data from MongoDB: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"Failed to fetch data from database: {str(e)}"
        }), 500