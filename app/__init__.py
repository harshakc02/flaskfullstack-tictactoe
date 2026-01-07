from flask import Flask
import mysql.connector
import time
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    retries = 10
    while retries:
        try:
            return mysql.connector.connect(
                host=os.getenv("MYSQL_HOST"),
                user=os.getenv("MYSQL_USER"),
                password=os.getenv("MYSQL_PASSWORD"),
                database=os.getenv("MYSQL_DB")
            )
        except mysql.connector.Error as e:
            print(f"Waiting for MySQL... ({e})")
            retries -= 1
            time.sleep(3)

    raise Exception("❌ Could not connect to MySQL")

def init_db(mysql_conn):
    cursor = mysql_conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS match_history (
            id INT AUTO_INCREMENT PRIMARY KEY,
            player_x VARCHAR(100),
            player_o VARCHAR(100),
            winner VARCHAR(10),
            played_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    mysql_conn.commit()
    cursor.close()

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")

    # Connect to DB (with retry)
    app.mysql = get_db_connection()

    # Auto-create tables
    init_db(app.mysql)

    # Register routes
    from .routes import main
    app.register_blueprint(main)

    return app
