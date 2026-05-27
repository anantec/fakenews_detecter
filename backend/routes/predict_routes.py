from flask import Blueprint, request, jsonify
import pickle
import os

predict = Blueprint("predict", __name__)

model = None
vectorizer = None

try:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    model_path = os.path.join(BASE_DIR, "model.pkl")
    vectorizer_path = os.path.join(BASE_DIR, "vectorizer.pkl")

    with open(model_path, "rb") as f:
        model = pickle.load(f)

    with open(vectorizer_path, "rb") as f:
        vectorizer = pickle.load(f)

    print("✅ Model + Vectorizer Loaded")

except Exception as e:
    print("❌ Error:", e)


@predict.route("/", methods=["POST"])
def predict_route():
    try:
        if model is None or vectorizer is None:
            return jsonify({"error": "Model not loaded"}), 500

        data = request.get_json()

        if not data or "news" not in data:
            return jsonify({"error": "News text required"}), 400

        news_text = data["news"]

        # TEXT → VECTOR
        transformed = vectorizer.transform([news_text])

        prediction = model.predict(transformed)[0]
        probability = model.predict_proba(transformed)[0]

        confidence = round(max(probability) * 100, 2)

        result = "Real News" if prediction == 1 else "Fake News"

        return jsonify({
            "prediction": result,
            "confidence": f"{confidence}%"
        }), 200

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500