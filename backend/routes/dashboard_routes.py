from flask import Blueprint, jsonify

dashboard = Blueprint("dashboard", __name__)

@dashboard.route("/", methods=["GET"])
def dashboard_home():

    try:
        return jsonify({
            "message": "Dashboard API working"
        }), 200

    except Exception as e:
        return jsonify({
            "message": "Internal server error",
            "error": str(e)
        }), 500