StudyBuddy - AI-Powered Adaptive Study Companion
=================================================

QUICK START (Standalone Dashboard)
----------------------------------
1. Open index.html directly in any modern web browser.
   - Double-click the file, or
   - Right-click > Open With > your browser, or
   - Drag the file into a browser window.

2. The dashboard works entirely offline with local score calculation.
   No server or installation required.

3. Use the sidebar to navigate between Dashboard, Predictions,
   Recommendations, History, and Settings.

4. The "Export Logs" button (bottom-right) downloads all telemetry
   events as a JSON file. You will be prompted for a participant ID.


OPTIONAL: Running the Flask API
--------------------------------
The Flask API (app_api.py) provides server-side prediction. The
dashboard will automatically use it when available and fall back to
local calculation when it is not.

Prerequisites:
   pip install flask flask-cors

Optional (for AutoGluon model inference):
   pip install autogluon

Start the server:
   python app_api.py

The API runs on http://localhost:5001 with two endpoints:
   GET  /health   - Returns server and model status.
   POST /predict  - Accepts student features as JSON, returns
                    predicted score, confidence interval, and
                    recommendations.

If an AutoGluon model exists at ../model/AutogluonModels (relative to
app_api.py), it will be loaded automatically. Otherwise the API uses
the same linear fallback formula as the standalone dashboard.

Example prediction request:
   curl -X POST http://localhost:5001/predict \
     -H "Content-Type: application/json" \
     -d '{
       "study_hours_per_week": 12,
       "attendance_rate": 92,
       "previous_gpa": 3.2,
       "assignment_completion_rate": 80,
       "class_participation": 6,
       "sleep_hours_avg": 7,
       "extracurricular_hours": 5,
       "stress_level": 5,
       "study_method": "mixed",
       "resource_usage": 6
     }'
