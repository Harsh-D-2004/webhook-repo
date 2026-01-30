from flask import Flask

from app.webhook.routes import webhook
from app.extensions import mongo

# create flask app
def create_app():

    app = Flask(__name__)

    # configure mongodb connection
    app.config["MONGO_URI"] = "mongodb+srv://hdoshi319:root%40123@cluster0.cerjo9c.mongodb.net/github"
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
