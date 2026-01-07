from flask import Flask
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()  # loads .env file

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')

    # MySQL connection
    app.mysql = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DB")
    )

    # Register Blueprints
    from .routes import main
    app.register_blueprint(main)

    return app
