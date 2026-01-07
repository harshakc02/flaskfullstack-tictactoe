import os

print("MYSQL_PASSWORD from env:", os.getenv("MYSQL_PASSWORD"))  # 👈 TEMP

class Config:
    MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_USER = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "password")
    MYSQL_DB = os.getenv("MYSQL_DB", "tic_tac_toe_db")
