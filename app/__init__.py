from flask import Flask

from app.webhook.routes import webhook
from app.extensions import mongo
import os

# create flask app
def create_app():

    app = Flask(__name__)

    # configure mongodb connection
    app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
    mongo.init_app(app)

    # test mongodb connection
    with app.app_context():
        try:
            assert mongo.db is not None
            mongo.db.command('ping')
            print("MongoDB Connection Successful!")
            print(f"Database: {mongo.db.name}")
        except Exception as e:
            print(f"MongoDB Connection Failed: {str(e)}")

    # register webhook blueprint
    app.register_blueprint(webhook)

    return app
