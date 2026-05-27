from flask import Flask
from flask_cors import CORS

from routes.auth_routes import auth
from routes.predict_routes import predict
from routes.dashboard_routes import dashboard

app = Flask(__name__)
CORS(app)

app.register_blueprint(auth, url_prefix="/auth")
app.register_blueprint(predict, url_prefix="/predict")
app.register_blueprint(dashboard, url_prefix="/dashboard")

@app.route("/")
def home():
    return "Backend Running ✅"

if __name__ == "__main__":
    app.run(debug=True)