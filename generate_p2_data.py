#!/usr/bin/env python3
"""
Generate all dummy data for Project 2 (StudyBuddy).
Uses numpy seed 43 for reproducibility.
"""

import numpy as np
import pandas as pd
import json
import os
from datetime import datetime, timedelta

np.random.seed(43)

# ============================================================
# Paths
# ============================================================
BASE = "/home/user/empty3/deliverables/project2"
SURVEY_PATH = os.path.join(BASE, "survey", "requirements_survey_responses.csv")
DATASET_PATH = os.path.join(BASE, "dataset", "student_performance_dataset.csv")
POSTTEST_PATH = os.path.join(BASE, "posttest", "posttest_survey_responses.csv")
LOGS_PATH = os.path.join(BASE, "logs", "interaction_logs.json")
QUALITATIVE_PATH = os.path.join(BASE, "posttest", "coded_qualitative_data.csv")

# ============================================================
# Helper functions
# ============================================================

def clamp(arr, lo, hi):
    return np.clip(arr, lo, hi)

def clamp_int(arr, lo, hi):
    return np.clip(np.round(arr).astype(int), lo, hi)

def pick(options, n, p=None):
    return np.random.choice(options, size=n, p=p).tolist()

# ============================================================
# Text pools
# ============================================================

open_feedback_pool = [
    "I would love a study tool that helps me plan my week and gives me personalized suggestions based on my performance trends.",
    "An AI study tool should be transparent about how it makes predictions so I can trust its recommendations for my coursework.",
    "I want something that tracks my study habits over time and tells me what is actually working versus what is wasting my time.",
    "It would be great to have a dashboard that shows my progress clearly with charts and motivational milestones to keep me on track.",
    "I really need help with time management and would love an AI that can suggest optimal study schedules based on my upcoming deadlines.",
    "A study AI should understand different learning styles and adapt its recommendations accordingly rather than giving generic advice to everyone.",
    "I am concerned about data privacy but I would use an AI study tool if it gave me full control over what data is collected and stored.",
    "The most important feature for me would be accurate grade predictions so I know where I stand and can adjust my effort accordingly.",
    "I want peer comparison features but only if they are anonymous because I do not want to feel judged by other students in my classes.",
    "An ideal study tool would integrate with my existing apps like Google Calendar and my university LMS to reduce the friction of using it.",
    "I think AI recommendations could help me discover better study methods since I have been using the same approach since high school.",
    "The tool should send me smart notifications before exams with targeted review suggestions instead of generic reminders that I will just ignore.",
    "I would appreciate a feature that breaks down large assignments into smaller tasks and helps me track completion over several weeks.",
    "Having a study buddy matching feature powered by AI would be amazing so I can find classmates who complement my strengths and weaknesses.",
    "I want the tool to explain why it recommends certain study strategies so I can learn to make better decisions on my own over time.",
    "A good study AI should recognize when I am burned out and suggest breaks or lighter study sessions instead of pushing me harder.",
    "I would use a study tool daily if it had a clean simple interface that does not overwhelm me with too many options or data points.",
    "The tool should help me identify which topics I struggle with the most and prioritize those in my study plan automatically.",
    "I think gamification elements like streaks and badges could make studying more engaging but they should not feel childish or forced.",
    "An AI study assistant should provide actionable feedback not just tell me my grade is low but explain specifically what I can improve.",
    "I want a tool that helps me balance academics with extracurriculars because I always end up sacrificing one for the other.",
    "It is important that the tool works offline too since I often study in places with unreliable internet connections on campus.",
    "I would trust the AI more if it showed me the data behind its predictions and let me correct it when it gets something wrong.",
    "A weekly summary email showing my study patterns and upcoming tasks would be really helpful for staying organized throughout the semester.",
    "I need something that adapts to my energy levels throughout the day and suggests the right type of studying for morning versus evening sessions.",
]

open_positive_pool = [
    "The dashboard was really intuitive and I liked how it visualized my study patterns over the past few weeks clearly.",
    "I found the grade prediction feature very motivating because it showed me how small changes in effort could improve my outcomes.",
    "The recommendation system felt personalized and relevant to my actual courses which made me trust it more than I expected.",
    "I appreciated how the tool explained its suggestions rather than just telling me what to do without any reasoning behind it.",
    "The interface was clean and easy to navigate even on my first time using it without needing any tutorial or guidance.",
    "Having all my study data in one place was extremely convenient and saved me time compared to tracking things manually.",
    "The notification system was well balanced and did not feel intrusive while still keeping me on track with my study goals.",
    "I liked the progress visualization feature because seeing my improvement over time kept me motivated to continue using the tool.",
    "The study method recommendations actually introduced me to techniques I had not tried before and some of them worked really well.",
    "Overall the experience felt trustworthy because the tool was transparent about what data it was using and how it made predictions.",
    "The goal setting feature helped me break down my semester targets into manageable weekly objectives which reduced my anxiety.",
    "I was impressed by how quickly the system adapted to my study habits and started giving more relevant suggestions after just a few sessions.",
]

open_negative_pool = [
    "The predictions did not always feel accurate especially early on when the system did not have much data about my study habits.",
    "I was uncomfortable with how much personal data the tool seemed to require before I could even start using the basic features.",
    "Some of the study recommendations felt too generic and did not account for the specific demands of my major or course load.",
    "The loading times were frustrating especially when switching between different sections of the dashboard during a study session.",
    "I found the peer comparison feature demotivating because it made me feel behind even when I was doing well in my own terms.",
    "The notification frequency was too high by default and I had to spend time adjusting settings before it became manageable.",
    "Some of the AI explanations were too technical and hard to understand which made me question whether the recommendations were valid.",
    "The tool did not integrate well with my existing study workflow and felt like an additional burden rather than a time saver.",
    "I noticed the system sometimes repeated the same recommendations even after I had already tried them and they did not work for me.",
    "The mobile experience was not as smooth as the desktop version and some features were hard to access on a smaller screen.",
    "The accuracy of grade predictions fluctuated a lot between weeks which made it hard to rely on them for planning purposes.",
    "There was no easy way to provide feedback on recommendations which meant the system could not learn from my actual preferences.",
]

open_suggestions_pool = [
    "Add a feature that lets students set their own confidence levels for predictions so the system knows when to be more cautious.",
    "Include a dark mode option because I often study late at night and the bright interface strains my eyes during evening sessions.",
    "Allow users to export their study data in standard formats so they can do their own analysis or share it with advisors.",
    "Implement a social feature where study groups can share goals and track collective progress on shared courses or projects.",
    "Add more granular privacy controls so students can choose exactly which data points are used for predictions and recommendations.",
    "Create a quick start guide or onboarding tutorial because the first time experience could be overwhelming for less tech savvy users.",
    "Include integration with popular calendar apps so study schedules and reminders sync automatically without manual data entry.",
    "Add a feature to compare different study strategies with evidence based explanations so students can make informed choices.",
    "Provide weekly summary reports via email for students who do not want to log in frequently but still want to stay informed.",
    "Allow customization of the dashboard layout so each student can prioritize the information that matters most to their workflow.",
    "Add accessibility features like screen reader support and high contrast themes to make the tool usable for all students.",
    "Include a way to temporarily pause data collection during breaks without losing historical data or resetting the AI model.",
]


# ============================================================
# FILE 1: Requirements Survey Responses (120 rows)
# ============================================================
print("Generating FILE 1: requirements_survey_responses.csv ...")

n1 = 120
participant_ids_1 = [f"P{i+1:03d}" for i in range(n1)]

ages = clamp_int(np.random.normal(22, 3, n1), 18, 45)
genders = pick(["Male", "Female", "Non-binary", "Prefer not to say"], n1, p=[0.45, 0.45, 0.06, 0.04])
education_levels = pick(
    ["Freshman", "Sophomore", "Junior", "Senior", "Graduate"], n1,
    p=[0.2, 0.2, 0.2, 0.2, 0.2]
)
major_categories = pick(
    ["STEM", "Humanities", "Social Sciences", "Business", "Arts"], n1,
    p=[0.35, 0.15, 0.2, 0.2, 0.1]
)
current_gpa = np.round(clamp(np.random.normal(3.2, 0.4, n1), 2.0, 4.0), 2)
study_hours_weekly = clamp_int(np.random.exponential(12, n1) + 1, 1, 40)
preferred_study_method = pick(["Visual", "Auditory", "Reading-Writing", "Kinesthetic"], n1, p=[0.35, 0.15, 0.35, 0.15])
tech_comfort = clamp_int(np.random.normal(5.0, 1.2, n1), 1, 7)
ai_trust_level = clamp_int(np.random.normal(3.8, 1.3, n1), 1, 7)
data_sharing_comfort = clamp_int(np.random.normal(3.5, 1.4, n1), 1, 7)
prediction_usefulness = clamp_int(np.random.normal(5.0, 1.1, n1), 1, 7)
recommendation_preference = pick(["Detailed", "Summary", "Visual", "Notification"], n1, p=[0.3, 0.3, 0.25, 0.15])
dashboard_complexity = pick(["Simple", "Moderate", "Detailed"], n1, p=[0.25, 0.5, 0.25])
notification_frequency = pick(["Never", "Daily", "Weekly", "Before_Exams"], n1, p=[0.1, 0.25, 0.35, 0.3])

feat_perf_track = clamp_int(np.random.normal(3.8, 1.0, n1), 1, 5)
feat_study_rec = clamp_int(np.random.normal(4.0, 0.9, n1), 1, 5)
feat_peer_comp = clamp_int(np.random.normal(2.8, 1.2, n1), 1, 5)
feat_goal_set = clamp_int(np.random.normal(3.9, 1.0, n1), 1, 5)
feat_prog_vis = clamp_int(np.random.normal(4.1, 0.9, n1), 1, 5)
privacy_concern_level = clamp_int(np.random.normal(4.5, 1.3, n1), 1, 7)

open_feedback = [open_feedback_pool[i % len(open_feedback_pool)] for i in np.random.permutation(n1)]

df1 = pd.DataFrame({
    "participant_id": participant_ids_1,
    "age": ages,
    "gender": genders,
    "education_level": education_levels,
    "major_category": major_categories,
    "current_gpa": current_gpa,
    "study_hours_weekly": study_hours_weekly,
    "preferred_study_method": preferred_study_method,
    "tech_comfort": tech_comfort,
    "ai_trust_level": ai_trust_level,
    "data_sharing_comfort": data_sharing_comfort,
    "prediction_usefulness": prediction_usefulness,
    "recommendation_preference": recommendation_preference,
    "dashboard_complexity": dashboard_complexity,
    "notification_frequency": notification_frequency,
    "feature_priority_performance_tracking": feat_perf_track,
    "feature_priority_study_recommendations": feat_study_rec,
    "feature_priority_peer_comparison": feat_peer_comp,
    "feature_priority_goal_setting": feat_goal_set,
    "feature_priority_progress_visualization": feat_prog_vis,
    "privacy_concern_level": privacy_concern_level,
    "open_feedback": open_feedback,
})

df1.to_csv(SURVEY_PATH, index=False)
print(f"  -> Saved {len(df1)} rows to {SURVEY_PATH}")


# ============================================================
# FILE 2: Student Performance Dataset (500 rows)
# ============================================================
print("Generating FILE 2: student_performance_dataset.csv ...")

n2 = 500
student_ids = [f"STU{i+1:04d}" for i in range(n2)]

study_hours = np.round(clamp(np.random.normal(15, 8, n2), 1, 40), 1)
attendance_rate = np.round(clamp(np.random.beta(6, 2, n2), 0.5, 1.0), 3)
previous_gpa = np.round(clamp(np.random.normal(3.0, 0.5, n2), 2.0, 4.0), 2)
assignment_completion = np.round(clamp(np.random.beta(5, 2, n2), 0.3, 1.0), 3)
class_participation = clamp_int(np.random.normal(6, 2, n2), 1, 10)
sleep_hours = np.round(clamp(np.random.normal(7, 1.2, n2), 4, 10), 1)
extracurricular_hours = np.round(clamp(np.random.exponential(5, n2), 0, 20), 1)
stress_level = clamp_int(np.random.normal(5.5, 2, n2), 1, 10)
study_method = pick(["Visual", "Auditory", "Reading-Writing", "Kinesthetic"], n2, p=[0.35, 0.15, 0.35, 0.15])
resource_usage = clamp_int(np.random.normal(6, 2, n2), 1, 10)

# Quiz score: correlated with study_hours, attendance, gpa, sleep
quiz_base = (
    0.25 * (study_hours / 40.0) +
    0.25 * ((attendance_rate - 0.5) / 0.5) +
    0.20 * ((previous_gpa - 2.0) / 2.0) +
    0.15 * ((sleep_hours - 4.0) / 6.0) +
    0.10 * ((assignment_completion - 0.3) / 0.7) +
    0.05 * (class_participation / 10.0)
)
quiz_score = np.round(clamp(quiz_base * 80 + 20 + np.random.normal(0, 8, n2), 0, 100), 1)

df2 = pd.DataFrame({
    "student_id": student_ids,
    "study_hours_per_week": study_hours,
    "attendance_rate": attendance_rate,
    "previous_gpa": previous_gpa,
    "assignment_completion_rate": assignment_completion,
    "class_participation_score": class_participation,
    "sleep_hours_avg": sleep_hours,
    "extracurricular_hours": extracurricular_hours,
    "stress_level": stress_level,
    "study_method": study_method,
    "resource_usage_score": resource_usage,
    "quiz_score": quiz_score,
})

df2.to_csv(DATASET_PATH, index=False)
print(f"  -> Saved {len(df2)} rows to {DATASET_PATH}")


# ============================================================
# FILE 3: Post-test Survey Responses (40 rows)
# ============================================================
print("Generating FILE 3: posttest_survey_responses.csv ...")

n3 = 40
participant_ids_3 = [f"P{i+1:03d}" for i in range(n3)]
ages_3 = clamp_int(np.random.normal(22, 3, n3), 18, 45)
genders_3 = pick(["Male", "Female", "Non-binary", "Prefer not to say"], n3, p=[0.45, 0.45, 0.06, 0.04])

# SUS: 10 questions, odd items positive (target high), even items negative (target low)
# targeting SUS ~ 68
# For odd items (q1,q3,q5,q7,q9): contribution = item - 1; mean item ~ 3.7 -> contrib ~2.7
# For even items (q2,q4,q6,q8,q10): contribution = 5 - item; mean item ~ 2.3 -> contrib ~2.7
# SUS = sum_of_contributions * 2.5; 10 items * 2.7 * 2.5 = 67.5 ~ 68
sus_data = {}
for q in range(1, 11):
    if q % 2 == 1:  # odd = positive
        sus_data[f"sus_q{q}"] = clamp_int(np.random.normal(3.7, 0.8, n3), 1, 5)
    else:  # even = negative
        sus_data[f"sus_q{q}"] = clamp_int(np.random.normal(2.3, 0.8, n3), 1, 5)

trust_data = {}
for q in range(1, 6):
    trust_data[f"trust_q{q}"] = clamp_int(np.random.normal(4.5, 1.2, n3), 1, 7)

usefulness_data = {}
for q in range(1, 6):
    usefulness_data[f"usefulness_q{q}"] = clamp_int(np.random.normal(5.0, 1.1, n3), 1, 7)

ease_data = {}
for q in range(1, 6):
    ease_data[f"ease_q{q}"] = clamp_int(np.random.normal(5.2, 1.0, n3), 1, 7)

accuracy_data = {}
for q in range(1, 4):
    accuracy_data[f"accuracy_perception_q{q}"] = clamp_int(np.random.normal(4.3, 1.3, n3), 1, 7)

privacy_data = {}
for q in range(1, 4):
    privacy_data[f"privacy_concern_q{q}"] = clamp_int(np.random.normal(4.5, 1.4, n3), 1, 7)

open_pos = [open_positive_pool[i % len(open_positive_pool)] for i in np.random.permutation(n3)]
open_neg = [open_negative_pool[i % len(open_negative_pool)] for i in np.random.permutation(n3)]
open_sug = [open_suggestions_pool[i % len(open_suggestions_pool)] for i in np.random.permutation(n3)]

df3_dict = {
    "participant_id": participant_ids_3,
    "age": ages_3,
    "gender": genders_3,
}
df3_dict.update(sus_data)
df3_dict.update(trust_data)
df3_dict.update(usefulness_data)
df3_dict.update(ease_data)
df3_dict.update(accuracy_data)
df3_dict.update(privacy_data)
df3_dict["open_positive"] = open_pos
df3_dict["open_negative"] = open_neg
df3_dict["open_suggestions"] = open_sug

df3 = pd.DataFrame(df3_dict)
df3.to_csv(POSTTEST_PATH, index=False)
print(f"  -> Saved {len(df3)} rows to {POSTTEST_PATH}")


# ============================================================
# FILE 4: Interaction Logs (40 entries, JSON)
# ============================================================
print("Generating FILE 4: interaction_logs.json ...")

n4 = 40
event_types = [
    "page_view", "button_click", "prediction_view", "recommendation_click",
    "filter_change", "dashboard_scroll", "settings_change", "tooltip_hover",
    "graph_interaction", "feature_toggle", "search_query", "export_data",
]
pages = [
    "dashboard", "predictions", "recommendations", "study_plan",
    "performance_history", "settings", "profile", "peer_comparison",
    "goal_tracker", "resource_library",
]
features_all = [
    "grade_prediction", "study_recommendations", "performance_dashboard",
    "goal_setting", "peer_comparison", "progress_visualization",
    "notification_settings", "study_timer", "resource_browser",
]
error_messages = [
    "Timeout loading predictions",
    "Failed to refresh dashboard data",
    "Chart rendering error",
    "Network connection interrupted",
    "Session token expired",
]

base_date = datetime(2026, 1, 15, 8, 0, 0)

logs = []
for i in range(n4):
    pid = f"P{i+1:03d}"
    # Random session start within a 2-week window
    offset_hours = int(np.random.uniform(0, 14 * 24))
    session_start = base_date + timedelta(hours=offset_hours, minutes=int(np.random.randint(0, 60)))
    duration = int(np.random.uniform(600, 2700))
    session_end = session_start + timedelta(seconds=duration)

    num_events = int(np.random.randint(10, 36))
    events = []
    pred_viewed = 0
    rec_clicked = 0
    current_time = session_start + timedelta(seconds=int(np.random.uniform(2, 15)))

    for e in range(num_events):
        etype = np.random.choice(event_types)
        page = np.random.choice(pages)
        time_on_page = round(float(np.random.uniform(5, 120)), 1)

        detail_options = [
            f"Viewed {page} section",
            f"Clicked on {np.random.choice(['chart', 'table', 'card', 'link', 'button'])}",
            f"Filtered by {np.random.choice(['date', 'course', 'metric', 'category'])}",
            f"Scrolled to {np.random.choice(['top', 'bottom', 'middle'])} of page",
            f"Hovered over {np.random.choice(['grade prediction', 'study tip', 'progress bar', 'metric card'])}",
            f"Toggled {np.random.choice(['dark mode', 'notifications', 'detailed view', 'compact mode'])}",
        ]
        detail = str(np.random.choice(detail_options))

        if etype == "prediction_view":
            pred_viewed += 1
        if etype == "recommendation_click":
            rec_clicked += 1

        events.append({
            "timestamp": current_time.isoformat(),
            "event_type": etype,
            "page": page,
            "details": detail,
            "time_on_page_seconds": time_on_page,
        })
        current_time += timedelta(seconds=int(np.random.uniform(5, max(6, duration // num_events * 2))))
        if current_time > session_end:
            current_time = session_end - timedelta(seconds=1)

    total_clicks = int(np.random.randint(max(15, num_events), num_events * 3 + 1))
    feats = list(np.random.choice(features_all, size=int(np.random.randint(2, 7)), replace=False))

    num_errors = int(np.random.choice([0, 0, 0, 0, 0, 1, 1, 2], p=[0.4, 0.1, 0.1, 0.05, 0.05, 0.15, 0.1, 0.05]))
    errors = []
    for _ in range(num_errors):
        err_time = session_start + timedelta(seconds=int(np.random.uniform(30, duration - 30)))
        errors.append({
            "timestamp": err_time.isoformat(),
            "error_message": str(np.random.choice(error_messages)),
        })

    logs.append({
        "participant_id": pid,
        "session_start": session_start.isoformat(),
        "session_end": session_end.isoformat(),
        "session_duration_seconds": duration,
        "total_clicks": total_clicks,
        "events": events,
        "predictions_viewed": pred_viewed,
        "recommendations_clicked": rec_clicked,
        "features_interacted": feats,
        "errors_encountered": errors,
    })

with open(LOGS_PATH, "w") as f:
    json.dump(logs, f, indent=2)
print(f"  -> Saved {len(logs)} entries to {LOGS_PATH}")


# ============================================================
# FILE 5: Coded Qualitative Data
# ============================================================
print("Generating FILE 5: coded_qualitative_data.csv ...")

themes = ["Trust & Transparency", "Usability", "AI Accuracy", "Privacy", "Engagement & Motivation"]

# Mapping of codes to themes
code_theme_map = {
    # Trust & Transparency
    "transparency_of_predictions": "Trust & Transparency",
    "explainability_of_recommendations": "Trust & Transparency",
    "trust_building_through_data": "Trust & Transparency",
    "user_control_over_AI": "Trust & Transparency",
    "clear_communication_of_AI_logic": "Trust & Transparency",
    # Usability
    "intuitive_interface": "Usability",
    "navigation_ease": "Usability",
    "onboarding_experience": "Usability",
    "mobile_responsiveness": "Usability",
    "dashboard_layout": "Usability",
    "loading_performance": "Usability",
    # AI Accuracy
    "prediction_accuracy": "AI Accuracy",
    "recommendation_relevance": "AI Accuracy",
    "personalization_quality": "AI Accuracy",
    "adaptation_over_time": "AI Accuracy",
    # Privacy
    "data_collection_concern": "Privacy",
    "data_sharing_control": "Privacy",
    "privacy_settings_granularity": "Privacy",
    "anonymity_in_comparisons": "Privacy",
    # Engagement & Motivation
    "motivational_features": "Engagement & Motivation",
    "progress_visualization_value": "Engagement & Motivation",
    "goal_setting_support": "Engagement & Motivation",
    "notification_effectiveness": "Engagement & Motivation",
    "gamification_appeal": "Engagement & Motivation",
}

codes_list = list(code_theme_map.keys())

# Positive text -> likely codes
positive_codes = [
    "intuitive_interface", "navigation_ease", "prediction_accuracy",
    "recommendation_relevance", "transparency_of_predictions",
    "progress_visualization_value", "personalization_quality",
    "trust_building_through_data", "notification_effectiveness",
    "dashboard_layout", "goal_setting_support", "adaptation_over_time",
]
negative_codes = [
    "prediction_accuracy", "data_collection_concern", "recommendation_relevance",
    "loading_performance", "mobile_responsiveness", "notification_effectiveness",
    "personalization_quality", "onboarding_experience", "anonymity_in_comparisons",
    "adaptation_over_time", "explainability_of_recommendations", "data_sharing_control",
]
suggestion_codes = [
    "privacy_settings_granularity", "data_sharing_control", "dashboard_layout",
    "gamification_appeal", "mobile_responsiveness", "onboarding_experience",
    "notification_effectiveness", "transparency_of_predictions", "motivational_features",
    "user_control_over_AI", "clear_communication_of_AI_logic", "progress_visualization_value",
]

coders = ["LLM_coder_1", "LLM_coder_2"]
# ~82% agreement -> 18% disagreement
agreement_rate = 0.82

qual_rows = []
for i in range(n4):
    pid = f"P{i+1:03d}"

    # Positive response
    pos_text = open_positive_pool[i % len(open_positive_pool)]
    pos_code = np.random.choice(positive_codes)
    pos_theme = code_theme_map[pos_code]
    coder1 = "LLM_coder_1"
    # For agreement simulation, both coders code same row; we record one row per coder
    # But simpler: record one row per response with the coder, and sometimes they disagree
    # We'll generate 2 rows per response (one per coder)
    if np.random.random() < agreement_rate:
        pos_code2 = pos_code
    else:
        pos_code2 = np.random.choice([c for c in positive_codes if c != pos_code])
    pos_theme2 = code_theme_map[pos_code2]

    qual_rows.append({
        "participant_id": pid, "response_type": "positive",
        "original_text": pos_text, "code": pos_code,
        "theme": pos_theme, "coder": "LLM_coder_1",
    })
    qual_rows.append({
        "participant_id": pid, "response_type": "positive",
        "original_text": pos_text, "code": pos_code2,
        "theme": pos_theme2, "coder": "LLM_coder_2",
    })

    # Negative response
    neg_text = open_negative_pool[i % len(open_negative_pool)]
    neg_code = np.random.choice(negative_codes)
    neg_theme = code_theme_map[neg_code]
    if np.random.random() < agreement_rate:
        neg_code2 = neg_code
    else:
        neg_code2 = np.random.choice([c for c in negative_codes if c != neg_code])
    neg_theme2 = code_theme_map[neg_code2]

    qual_rows.append({
        "participant_id": pid, "response_type": "negative",
        "original_text": neg_text, "code": neg_code,
        "theme": neg_theme, "coder": "LLM_coder_1",
    })
    qual_rows.append({
        "participant_id": pid, "response_type": "negative",
        "original_text": neg_text, "code": neg_code2,
        "theme": neg_theme2, "coder": "LLM_coder_2",
    })

    # Suggestion response
    sug_text = open_suggestions_pool[i % len(open_suggestions_pool)]
    sug_code = np.random.choice(suggestion_codes)
    sug_theme = code_theme_map[sug_code]
    if np.random.random() < agreement_rate:
        sug_code2 = sug_code
    else:
        sug_code2 = np.random.choice([c for c in suggestion_codes if c != sug_code])
    sug_theme2 = code_theme_map[sug_code2]

    qual_rows.append({
        "participant_id": pid, "response_type": "suggestion",
        "original_text": sug_text, "code": sug_code,
        "theme": sug_theme, "coder": "LLM_coder_1",
    })
    qual_rows.append({
        "participant_id": pid, "response_type": "suggestion",
        "original_text": sug_text, "code": sug_code2,
        "theme": sug_theme2, "coder": "LLM_coder_2",
    })

df5 = pd.DataFrame(qual_rows)
df5.to_csv(QUALITATIVE_PATH, index=False)
print(f"  -> Saved {len(df5)} rows to {QUALITATIVE_PATH}")


# ============================================================
# Verification summary
# ============================================================
print("\n=== Generation Complete ===")
print(f"FILE 1: {SURVEY_PATH}")
print(f"  Rows: {len(df1)}, Columns: {list(df1.columns)}")
print(f"FILE 2: {DATASET_PATH}")
print(f"  Rows: {len(df2)}, Columns: {list(df2.columns)}")
corr = df2[["study_hours_per_week", "attendance_rate", "previous_gpa", "sleep_hours_avg", "quiz_score"]].corr()
print(f"  Quiz score correlations:\n{corr['quiz_score'].to_string()}")
print(f"FILE 3: {POSTTEST_PATH}")
print(f"  Rows: {len(df3)}, Columns: {list(df3.columns)}")
# Calculate SUS scores
sus_cols_odd = [f"sus_q{q}" for q in [1,3,5,7,9]]
sus_cols_even = [f"sus_q{q}" for q in [2,4,6,8,10]]
sus_score = (df3[sus_cols_odd].sum(axis=1) - 5 + 25 - df3[sus_cols_even].sum(axis=1)) * 2.5
print(f"  Mean SUS score: {sus_score.mean():.1f} (target ~68)")
print(f"FILE 4: {LOGS_PATH}")
print(f"  Entries: {len(logs)}")
print(f"FILE 5: {QUALITATIVE_PATH}")
print(f"  Rows: {len(df5)}")
agreements = sum(1 for i in range(0, len(qual_rows), 2) if qual_rows[i]["code"] == qual_rows[i+1]["code"])
total_pairs = len(qual_rows) // 2
print(f"  Coder agreement: {agreements}/{total_pairs} = {agreements/total_pairs:.1%}")
print("\nAll files generated successfully!")
