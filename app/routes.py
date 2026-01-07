from flask import Blueprint, render_template, request, jsonify
from app.models import save_match, get_match_history

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return render_template("index.html")

@main.route("/save-match", methods=["POST"])
def save_match_route():
    data = request.json
    save_match(
        data["player_x"],
        data["player_o"],
        data["winner"]
    )
    return jsonify({"status": "saved"})

@main.route("/history")
def history():
    return jsonify(get_match_history())
