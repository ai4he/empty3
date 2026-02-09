"""
StudyBuddy Flask API - AutoGluon Inference Server
Serves score predictions via POST /predict and health checks via GET /health.
Falls back to a simple linear formula if AutoGluon model is unavailable.
"""

import os
import json
import traceback
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# --------------- Model Loading ---------------
MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "model", "AutogluonModels")
predictor = None

try:
    from autogluon.tabular import TabularPredictor
    if os.path.isdir(MODEL_PATH):
        predictor = TabularPredictor.load(MODEL_PATH)
        print(f"[INFO] AutoGluon model loaded from {MODEL_PATH}")
    else:
        print(f"[WARN] Model directory not found at {MODEL_PATH}. Using fallback formula.")
except Exception as e:
    print(f"[WARN] Could not load AutoGluon: {e}. Using fallback formula.")


# --------------- Fallback Linear Formula ---------------
METHOD_BONUS = {
    "mixed": 0, "visual": 1, "reading": 0.5,
    "practice": 2, "group": 1.5,
}


def fallback_predict(features: dict) -> dict:
    """Simple linear weighted formula when AutoGluon is unavailable."""
    score = (
        features.get("study_hours_per_week", 10) * 1.2
        + features.get("attendance_rate", 85) * 0.25
        + features.get("previous_gpa", 3.0) * 10
        + features.get("assignment_completion_rate", 80) * 0.15
        + features.get("class_participation", 5) * 1.0
        + features.get("sleep_hours_avg", 7) * 0.8
        - features.get("extracurricular_hours", 5) * 0.3
        - features.get("stress_level", 5) * 1.5
        + METHOD_BONUS.get(features.get("study_method", "mixed"), 0)
        + features.get("resource_usage", 5) * 0.5
    )
    score = round(max(0, min(100, score)), 1)
    ci_half = round(max(3, 12 - features.get("resource_usage", 5)), 1)

    recommendations = generate_recommendations(features, score)

    return {
        "predicted_score": score,
        "confidence_interval": {
            "lower": round(max(0, score - ci_half), 1),
            "upper": round(min(100, score + ci_half), 1),
        },
        "recommendations": recommendations,
        "model": "fallback_linear",
    }


def generate_recommendations(features: dict, score: float) -> list:
    """Generate contextual study recommendations based on input features."""
    recs = []
    if features.get("study_hours_per_week", 10) < 10:
        recs.append("Increase weekly study hours to at least 10 for better retention.")
    if features.get("sleep_hours_avg", 7) < 7:
        recs.append("Aim for 7-8 hours of sleep to improve memory consolidation.")
    if features.get("stress_level", 5) > 6:
        recs.append("Consider stress-management techniques such as meditation or exercise.")
    if features.get("attendance_rate", 85) < 85:
        recs.append("Improving class attendance can significantly boost your performance.")
    if features.get("assignment_completion_rate", 80) < 75:
        recs.append("Focus on completing all assignments -- they contribute heavily to grades.")
    if features.get("class_participation", 5) < 4:
        recs.append("Participate more in class discussions to deepen understanding.")
    if score >= 80:
        recs.append("Great trajectory! Maintain your current habits and aim for excellence.")
    if not recs:
        recs.append("You are on track. Keep up the consistent effort!")
    return recs


# --------------- Routes ---------------

@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "model_loaded": predictor is not None,
        "model_type": "autogluon" if predictor else "fallback_linear",
    })


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json(force=True)
        if not data:
            return jsonify({"error": "No JSON body provided"}), 400

        required_fields = [
            "study_hours_per_week", "attendance_rate", "previous_gpa",
            "assignment_completion_rate", "class_participation",
            "sleep_hours_avg", "extracurricular_hours", "stress_level",
            "study_method", "resource_usage",
        ]
        missing = [f for f in required_fields if f not in data]
        if missing:
            return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

        # Try AutoGluon first
        if predictor is not None:
            import pandas as pd
            df = pd.DataFrame([data])
            prediction = float(predictor.predict(df).iloc[0])
            prediction = round(max(0, min(100, prediction)), 1)
            ci_half = 5.0  # default confidence interval for model
            recommendations = generate_recommendations(data, prediction)
            result = {
                "predicted_score": prediction,
                "confidence_interval": {
                    "lower": round(max(0, prediction - ci_half), 1),
                    "upper": round(min(100, prediction + ci_half), 1),
                },
                "recommendations": recommendations,
                "model": "autogluon",
            }
        else:
            result = fallback_predict(data)

        return jsonify(result)

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


# --------------- Entry Point ---------------

if __name__ == "__main__":
    print("[INFO] Starting StudyBuddy API on port 5001...")
    app.run(host="0.0.0.0", port=5001, debug=True)
