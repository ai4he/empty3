#!/usr/bin/env python3
"""
Generate cells for Sections 4-5 of the Human-Centered AI notebook.
Saves output as JSON at /home/user/empty3/notebook_part2.json.
"""

import json

def mk_md(source_str):
    """Create a markdown cell dict."""
    lines = source_str.split("\n")
    source = [line + "\n" for line in lines[:-1]] + [lines[-1]]
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": source,
        "outputs": []
    }

def mk_code(source_str):
    """Create a code cell dict."""
    lines = source_str.split("\n")
    source = [line + "\n" for line in lines[:-1]] + [lines[-1]]
    return {
        "cell_type": "code",
        "metadata": {},
        "source": source,
        "outputs": [],
        "execution_count": None
    }


cells = []

# ──────────────────────────────────────────────
# CELL 1 — Section 4 Header (markdown)
# ──────────────────────────────────────────────
cells.append(mk_md("""\
---
<a id="section-4"></a>
# Section 4: Deploy Prototype

## Deployment Strategy

Both prototypes are designed as **static web applications** that can be deployed with minimal infrastructure:

### Deployment Options (Simplest to Most Complex)

| Method | Complexity | Requirements | Best For |
|:---|:---|:---|:---|
| **Local file** | Trivial | Web browser only | Individual testing |
| **Python HTTP server** | Very Low | Python installed | Lab sessions |
| **GitHub Pages** | Low | GitHub account | Persistent hosting |
| **Netlify/Vercel** | Low | Account signup | Production-like |

### Telemetry Architecture

Both prototypes include client-side telemetry that captures:
1. **Navigation events** — Page views, timestamps, time-on-page
2. **Interaction events** — Clicks, form submissions, choices
3. **Feature usage** — Which features are accessed and how often
4. **Session metadata** — Duration, browser info, errors

Data is stored in the browser's memory (`window.telemetryLog` array) and exported as JSON files per participant. This approach:
- Requires **no server-side infrastructure** for logging
- Gives participants **full transparency** over collected data
- Enables **easy integration** with analysis pipelines
- Follows **data minimization** principles (GDPR-aligned)

### Methodological Consideration
For a CHI paper, using client-side telemetry is acceptable for prototype evaluations, but researchers should note:
- Data loss if participant closes browser before export
- No guarantee of timestamp accuracy across devices
- Mitigation: Use a standardized lab setup with supervised sessions

### References
- Barkhuus, L., & Rode, J. A. (2007). From mice to men–24 years of evaluation in CHI. *Proc. ACM CHI*.
- Dumais, S., et al. (2014). Understanding User Behavior Through Log Data and Analysis. *Ways of Knowing in HCI*, Springer."""))

# ──────────────────────────────────────────────
# CELL 2 — P1 Deployment (markdown + code)
# ──────────────────────────────────────────────
cells.append(mk_md("""\
## 4.1 Project 1: Deploying Gemini Quest

### Quick Start
1. Open `deliverables/project1/webapp/index.html` in any modern browser
2. Play through the game, making narrative choices
3. Click "Export Logs" to download interaction data as JSON

### For Lab Sessions
Run a simple HTTP server to serve the files:
```bash
cd deliverables/project1/webapp
python -m http.server 8080
# Open http://localhost:8080 in browser
```

### Telemetry Data Format
The exported JSON contains all interaction events structured for direct analysis pipeline input."""))

cells.append(mk_code("""\
# ============================================================
# PROJECT 1: Verify Deployment Files
# ============================================================
import webbrowser

p1_webapp = P1_DIR / 'webapp' / 'index.html'
print("=" * 60)
print("PROJECT 1: DEPLOYMENT VERIFICATION")
print("=" * 60)

if p1_webapp.exists():
    file_size = p1_webapp.stat().st_size
    print(f"\\n\\u2713 index.html exists ({file_size:,} bytes)")
    
    # Check for key components
    with open(p1_webapp, 'r') as f:
        content = f.read()
    
    checks = {
        'Telemetry logging': 'telemetryLog' in content,
        'Character creation': 'character' in content.lower(),
        'Chapter system': 'chapter' in content.lower(),
        'Export function': 'export' in content.lower() or 'download' in content.lower(),
        'CSS styling': '<style' in content,
        'JavaScript': '<script' in content
    }
    
    for check, passed in checks.items():
        status = "\\u2713" if passed else "\\u2717"
        print(f"  {status} {check}")
    
    print(f"\\n\\U0001f4cb To test locally:")
    print(f"   Option 1: Open the file directly in your browser")
    print(f"   Option 2: python -m http.server 8080 --directory {P1_DIR / 'webapp'}")
    
    # Show telemetry structure
    print(f"\\n\\U0001f4ca Expected telemetry output structure:")
    sample_telemetry = {
        "participant_id": "P001",
        "session_start": "2025-01-15T10:30:00.000Z",
        "session_end": "2025-01-15T11:05:00.000Z",
        "events": [
            {"timestamp": "...", "event_type": "page_view", "page": "intro", "time_on_page_seconds": 15},
            {"timestamp": "...", "event_type": "choice_made", "page": "chapter_1", "details": {"choice": "A"}}
        ]
    }
    print(json.dumps(sample_telemetry, indent=2))
else:
    print(f"\\n\\u2717 index.html not found at {p1_webapp}")
    print("  Generate it using the Gemini API (Section 3) or check the deliverables folder.")\
"""))

# ──────────────────────────────────────────────
# CELL 3 — P2 Deployment (markdown + code)
# ──────────────────────────────────────────────
cells.append(mk_md("""\
## 4.2 Project 2: Deploying StudyBuddy

### Quick Start (Static Only — No AI Backend)
1. Open `deliverables/project2/webapp/index.html` in any modern browser
2. The dashboard works standalone with simulated predictions
3. Click "Export Logs" to download interaction data

### Full Deployment (With AutoGluon Backend)
1. Install requirements:
   ```bash
   pip install flask flask-cors autogluon
   ```
2. Train the model (run Section 3.2 in this notebook)
3. Start the Flask API:
   ```bash
   python deliverables/project2/webapp/app_api.py
   ```
4. Open `index.html` — it will automatically connect to the API at `localhost:5001`

### API Endpoints
| Endpoint | Method | Description |
|:---|:---|:---|
| `/predict` | POST | Send student features, receive predicted score |
| `/health` | GET | Check if model is loaded |

### Mixed Methods Data Collection Strategy
For the usability evaluation, we collect data through **three complementary channels**:

1. **Telemetry logs** (automatic) — Behavioral data from prototype interaction
2. **Post-test survey** (manual) — Self-reported usability, trust, and perception
3. **Think-aloud protocol** (optional) — Verbal protocol for richer qualitative data

This triangulation strengthens the validity of our findings (Lazar et al., 2017)."""))

cells.append(mk_code("""\
# ============================================================
# PROJECT 2: Verify Deployment Files
# ============================================================
print("=" * 60)
print("PROJECT 2: DEPLOYMENT VERIFICATION")
print("=" * 60)

p2_webapp = P2_DIR / 'webapp' / 'index.html'
p2_api = P2_DIR / 'webapp' / 'app_api.py'

# Check web app
if p2_webapp.exists():
    file_size = p2_webapp.stat().st_size
    print(f"\\n\\u2713 index.html exists ({file_size:,} bytes)")
    
    with open(p2_webapp, 'r') as f:
        content = f.read()
    
    checks = {
        'Telemetry logging': 'telemetryLog' in content,
        'Dashboard page': 'dashboard' in content.lower(),
        'Prediction form': 'predict' in content.lower(),
        'Recommendations': 'recommend' in content.lower(),
        'Export function': 'export' in content.lower() or 'download' in content.lower(),
        'API endpoint reference': 'localhost:5001' in content or 'fetch' in content.lower(),
        'CSS styling': '<style' in content,
        'JavaScript': '<script' in content
    }
    
    for check, passed in checks.items():
        status = "\\u2713" if passed else "\\u2717"
        print(f"  {status} {check}")
else:
    print(f"\\n\\u2717 index.html not found at {p2_webapp}")

# Check API
if p2_api.exists():
    api_size = p2_api.stat().st_size
    print(f"\\n\\u2713 app_api.py exists ({api_size:,} bytes)")
    
    with open(p2_api, 'r') as f:
        api_content = f.read()
    
    api_checks = {
        'Flask app': 'Flask' in api_content,
        'CORS enabled': 'CORS' in api_content,
        'Predict endpoint': '/predict' in api_content,
        'Health endpoint': '/health' in api_content,
        'AutoGluon integration': 'autogluon' in api_content.lower() or 'TabularPredictor' in api_content,
        'Fallback predictor': 'fallback' in api_content.lower()
    }
    
    for check, passed in api_checks.items():
        status = "\\u2713" if passed else "\\u2717"
        print(f"  {status} {check}")
else:
    print(f"\\n\\u2717 app_api.py not found at {p2_api}")

# Model check
model_path = P2_DIR / 'model' / 'AutogluonModels'
if model_path.exists():
    print(f"\\n\\u2713 AutoGluon model directory exists: {model_path}")
else:
    print(f"\\n\\u2139 AutoGluon model not yet trained. Run Section 3.2 to train.")
    print("  The Flask API includes a fallback linear predictor that works without the model.")

print(f"\\n\\U0001f4cb Deployment commands:")
print(f"   Static only: Open {p2_webapp} in browser")
print(f"   With API:    python {p2_api}")
print(f"   Test API:    curl -X POST http://localhost:5001/predict -H 'Content-Type: application/json' \\\\")
print(f"                -d '{{\\\"study_hours_per_week\\\": 15, \\\"attendance_rate\\\": 0.9, \\\"previous_gpa\\\": 3.2}}'\")\
"""))

# ──────────────────────────────────────────────
# CELL 4 — Section 5 Header (markdown)
# ──────────────────────────────────────────────
cells.append(mk_md("""\
---
<a id="section-5"></a>
# Section 5: User Evaluation

## Methodology: Mixed-Methods Usability Evaluation

Following established HCI evaluation practices (Lazar et al., 2017), we conduct a **within-subjects usability evaluation** combining:

### Standardized Instruments

1. **System Usability Scale (SUS)** — Brooke (1996)
   - 10-item questionnaire, 5-point Likert scale
   - Produces a single score (0-100)
   - Industry benchmark: 68 = "OK", 80+ = "Good"
   - Widely used and validated in HCI research

2. **User Engagement Scale Short Form (UES-SF)** — O'Brien et al. (2018) [Project 1]
   - Subscales: Focused Attention (FA), Perceived Usability (PU), Aesthetic Appeal (AE), Reward Factor (RW)
   - 5-point Likert scale

3. **Trust in AI Scale** — Adapted from Madsen & Gregor (2000) [Project 2]
   - 5 items measuring perceived reliability, competence, and benevolence
   - 7-point Likert scale

4. **Technology Acceptance Model (TAM)** — Davis (1989) [Project 2]
   - Perceived Usefulness (5 items) and Perceived Ease of Use (5 items)
   - 7-point Likert scale

5. **Custom Scales** (validated via pilot study):
   - Narrative Quality (5 items, 7-point) [Project 1]
   - AI Perception (5 items, 7-point) [Project 1]
   - Immersion (3 items, 7-point) [Project 1]
   - Accuracy Perception (3 items, 7-point) [Project 2]
   - Privacy Concern (3 items, 7-point) [Project 2]

### Qualitative Data Collection
- **Open-ended survey items:** Positive feedback, negative feedback, suggestions
- **Think-aloud protocol** (optional): Participants verbalize thoughts during interaction
- **Behavioral telemetry:** Automatic logging from prototype

### Evaluation Protocol
1. Informed consent and demographics (5 min)
2. Brief tutorial on the prototype (2 min)
3. Free exploration / task completion (15-30 min)
4. Post-test survey completion (10-15 min)
5. Optional debrief interview (5 min)

Total session time: ~45 minutes

### References
- Brooke, J. (1996). SUS: A 'quick and dirty' usability scale. *Usability Evaluation in Industry*.
- O'Brien, H. L., Cairns, P., & Hall, M. (2018). A practical approach to measuring user engagement with the refined user engagement scale (UES) and new UES short form. *IJHCS*, 112, 28-39.
- Davis, F. D. (1989). Perceived usefulness, perceived ease of use, and user acceptance of information technology. *MIS Quarterly*, 13(3), 319-340.
- Madsen, M., & Gregor, S. (2000). Measuring human-computer trust. *Proc. Australasian Conference on Information Systems*."""))

# ──────────────────────────────────────────────
# CELL 5 — P1 Post-test Survey and Data (markdown + code)
# ──────────────────────────────────────────────
cells.append(mk_md("""\
## 5.1 Project 1: Gemini Quest — Post-Test Evaluation

### Post-Test Survey Instrument

**Part A: System Usability Scale (SUS)** — 5-point Likert (Strongly Disagree to Strongly Agree)
1. I think that I would like to use this system frequently.
2. I found the system unnecessarily complex. (R)
3. I thought the system was easy to use.
4. I think that I would need the support of a technical person to use this system. (R)
5. I found the various functions in this system were well integrated.
6. I thought there was too much inconsistency in this system. (R)
7. I would imagine that most people would learn to use this system very quickly.
8. I found the system very cumbersome to use. (R)
9. I felt very confident using the system.
10. I needed to learn a lot of things before I could get going with this system. (R)

*(R) = Reverse-coded items*

**Part B: User Engagement Scale - Short Form (UES-SF)** — 5-point Likert
- Focused Attention (FA): 5 items
- Perceived Usability (PU): 3 items
- Aesthetic Appeal (AE): 4 items
- Reward Factor (RW): 3 items

**Part C: Narrative Quality** — 7-point Likert
1. The story was engaging and held my attention.
2. The characters felt believable and interesting.
3. The world-building was rich and immersive.
4. My choices felt meaningful and impactful.
5. The story had good pacing and flow.

**Part D: AI Perception** — 7-point Likert
1. The AI-generated content felt natural and coherent.
2. I could not distinguish AI content from human-created content.
3. The AI enhanced my gaming experience.
4. I trust AI to create quality game content.
5. I would play more AI-generated games in the future.

**Part E: Immersion** — 7-point Likert
1. I lost track of time while playing.
2. I felt transported to the game world.
3. The experience was absorbing.

**Part F: Open-Ended Feedback**
- What did you enjoy most about the experience? (free text)
- What frustrated you or could be improved? (free text)
- Any other suggestions for improvement? (free text)"""))

cells.append(mk_code("""\
# ============================================================
# PROJECT 1: Load Post-Test Data and Interaction Logs
# ============================================================
# Load post-test survey
p1_posttest_path = P1_DIR / 'posttest' / 'posttest_survey_responses.csv'
p1_logs_path = P1_DIR / 'logs' / 'interaction_logs.json'

try:
    p1_posttest = pd.read_csv(p1_posttest_path)
    print(f"\\u2713 Loaded P1 post-test data: {p1_posttest.shape[0]} participants, {p1_posttest.shape[1]} columns")
except FileNotFoundError:
    print("\\u2717 Post-test file not found.")
    p1_posttest = None

# Load interaction logs
try:
    with open(p1_logs_path, 'r') as f:
        p1_logs = json.load(f)
    print(f"\\u2713 Loaded P1 interaction logs: {len(p1_logs)} participants")
except FileNotFoundError:
    print("\\u2717 Interaction logs not found.")
    p1_logs = None

# ---- Compute SUS Scores ----
if p1_posttest is not None:
    sus_cols = [f'sus_q{i}' for i in range(1, 11)]
    
    def compute_sus(row):
        \"\"\"Compute SUS score following Brooke (1996) scoring method.\"\"\"
        score = 0
        for i in range(1, 11):
            val = row[f'sus_q{i}']
            if i % 2 == 1:  # Odd items (positive): score - 1
                score += (val - 1)
            else:  # Even items (negative): 5 - score
                score += (5 - val)
        return score * 2.5  # Scale to 0-100
    
    p1_posttest['sus_score'] = p1_posttest.apply(compute_sus, axis=1)
    
    print(f"\\n{'='*60}")
    print("PROJECT 1: SUS SCORES")
    print("="*60)
    print(f"  Mean: {p1_posttest['sus_score'].mean():.1f}")
    print(f"  SD: {p1_posttest['sus_score'].std():.1f}")
    print(f"  Median: {p1_posttest['sus_score'].median():.1f}")
    print(f"  Range: [{p1_posttest['sus_score'].min():.1f}, {p1_posttest['sus_score'].max():.1f}]")
    
    # SUS Grade (Bangor et al., 2009)
    mean_sus = p1_posttest['sus_score'].mean()
    if mean_sus >= 80.3:
        grade = 'A (Excellent)'
    elif mean_sus >= 68:
        grade = 'B (Good)'
    elif mean_sus >= 51:
        grade = 'C (OK)'
    else:
        grade = 'D/F (Poor)'
    print(f"  SUS Grade: {grade}")

# ---- Summarize Interaction Logs ----
if p1_logs is not None:
    print(f"\\n{'='*60}")
    print("PROJECT 1: INTERACTION LOG SUMMARY")
    print("="*60)
    
    durations = [p['session_duration_seconds'] for p in p1_logs]
    clicks = [p['total_clicks'] for p in p1_logs]
    pages = [p['total_pages_visited'] for p in p1_logs]
    n_events = [len(p['events']) for p in p1_logs]
    n_choices = [len(p.get('choices_made', [])) for p in p1_logs]
    
    print(f"  Session duration: M={np.mean(durations):.0f}s (SD={np.std(durations):.0f}s)")
    print(f"  Total clicks: M={np.mean(clicks):.1f} (SD={np.std(clicks):.1f})")
    print(f"  Pages visited: M={np.mean(pages):.1f} (SD={np.std(pages):.1f})")
    print(f"  Events logged: M={np.mean(n_events):.1f} (SD={np.std(n_events):.1f})")
    print(f"  Choices made: M={np.mean(n_choices):.1f} (SD={np.std(n_choices):.1f})")
    
    errors = [len(p.get('errors_encountered', [])) for p in p1_logs]
    print(f"  Errors encountered: M={np.mean(errors):.1f} (SD={np.std(errors):.1f})")\
"""))

# ──────────────────────────────────────────────
# CELL 6 — P2 Post-test Survey and Data (markdown + code)
# ──────────────────────────────────────────────
cells.append(mk_md("""\
## 5.2 Project 2: StudyBuddy — Post-Test Evaluation

### Post-Test Survey Instrument

**Part A: System Usability Scale (SUS)** — Same as Project 1

**Part B: Trust in AI** — 7-point Likert (Strongly Disagree to Strongly Agree)
1. I believe the system's predictions are reliable.
2. I feel confident in the system's recommendations.
3. The system seems competent at predicting academic performance.
4. I can depend on the system to help me study effectively.
5. The system has my best interests in mind.

**Part C: Perceived Usefulness (TAM)** — 7-point Likert
1. Using this system would improve my academic performance.
2. Using this system would increase my study productivity.
3. Using this system would make studying more effective.
4. I find this system useful for academic planning.
5. Using this system would give me greater control over my studies.

**Part D: Perceived Ease of Use (TAM)** — 7-point Likert
1. Learning to use this system was easy.
2. I find it easy to get the system to do what I want.
3. The system interface is clear and understandable.
4. The system is flexible to interact with.
5. It is easy to become skillful at using this system.

**Part E: Accuracy Perception** — 7-point Likert
1. The predicted scores seem accurate.
2. The recommendations are relevant to my situation.
3. I would trust these predictions for making study decisions.

**Part F: Privacy Concern** — 7-point Likert
1. I am concerned about the privacy of my academic data.
2. I worry about how my data might be used beyond this system.
3. I would want more control over what data the system collects.

**Part G: Open-Ended Feedback**
- What did you find most useful about StudyBuddy? (free text)
- What concerns or frustrations did you experience? (free text)
- How would you improve the system? (free text)"""))

cells.append(mk_code("""\
# ============================================================
# PROJECT 2: Load Post-Test Data and Interaction Logs
# ============================================================
p2_posttest_path = P2_DIR / 'posttest' / 'posttest_survey_responses.csv'
p2_logs_path = P2_DIR / 'logs' / 'interaction_logs.json'

try:
    p2_posttest = pd.read_csv(p2_posttest_path)
    print(f"\\u2713 Loaded P2 post-test data: {p2_posttest.shape[0]} participants, {p2_posttest.shape[1]} columns")
except FileNotFoundError:
    print("\\u2717 Post-test file not found.")
    p2_posttest = None

try:
    with open(p2_logs_path, 'r') as f:
        p2_logs = json.load(f)
    print(f"\\u2713 Loaded P2 interaction logs: {len(p2_logs)} participants")
except FileNotFoundError:
    print("\\u2717 Interaction logs not found.")
    p2_logs = None

# ---- Compute SUS Scores ----
if p2_posttest is not None:
    def compute_sus(row):
        score = 0
        for i in range(1, 11):
            val = row[f'sus_q{i}']
            if i % 2 == 1:
                score += (val - 1)
            else:
                score += (5 - val)
        return score * 2.5
    
    p2_posttest['sus_score'] = p2_posttest.apply(compute_sus, axis=1)
    
    print(f"\\n{'='*60}")
    print("PROJECT 2: SUS SCORES")
    print("="*60)
    print(f"  Mean: {p2_posttest['sus_score'].mean():.1f}")
    print(f"  SD: {p2_posttest['sus_score'].std():.1f}")
    print(f"  Median: {p2_posttest['sus_score'].median():.1f}")
    print(f"  Range: [{p2_posttest['sus_score'].min():.1f}, {p2_posttest['sus_score'].max():.1f}]")
    
    mean_sus = p2_posttest['sus_score'].mean()
    if mean_sus >= 80.3:
        grade = 'A (Excellent)'
    elif mean_sus >= 68:
        grade = 'B (Good)'
    elif mean_sus >= 51:
        grade = 'C (OK)'
    else:
        grade = 'D/F (Poor)'
    print(f"  SUS Grade: {grade}")

    # Trust scores
    trust_cols = [f'trust_q{i}' for i in range(1, 6)]
    if all(c in p2_posttest.columns for c in trust_cols):
        p2_posttest['trust_mean'] = p2_posttest[trust_cols].mean(axis=1)
        print(f"\\n  Trust in AI: M={p2_posttest['trust_mean'].mean():.2f}, SD={p2_posttest['trust_mean'].std():.2f}")
    
    # Usefulness scores
    use_cols = [f'usefulness_q{i}' for i in range(1, 6)]
    if all(c in p2_posttest.columns for c in use_cols):
        p2_posttest['usefulness_mean'] = p2_posttest[use_cols].mean(axis=1)
        print(f"  Perceived Usefulness: M={p2_posttest['usefulness_mean'].mean():.2f}, SD={p2_posttest['usefulness_mean'].std():.2f}")

    # Ease of use scores
    ease_cols = [f'ease_q{i}' for i in range(1, 6)]
    if all(c in p2_posttest.columns for c in ease_cols):
        p2_posttest['ease_mean'] = p2_posttest[ease_cols].mean(axis=1)
        print(f"  Perceived Ease of Use: M={p2_posttest['ease_mean'].mean():.2f}, SD={p2_posttest['ease_mean'].std():.2f}")

# ---- Summarize Interaction Logs ----
if p2_logs is not None:
    print(f"\\n{'='*60}")
    print("PROJECT 2: INTERACTION LOG SUMMARY")
    print("="*60)
    
    durations = [p['session_duration_seconds'] for p in p2_logs]
    clicks = [p['total_clicks'] for p in p2_logs]
    n_events = [len(p['events']) for p in p2_logs]
    predictions = [p.get('predictions_viewed', 0) for p in p2_logs]
    recommendations = [p.get('recommendations_clicked', 0) for p in p2_logs]
    
    print(f"  Session duration: M={np.mean(durations):.0f}s (SD={np.std(durations):.0f}s)")
    print(f"  Total clicks: M={np.mean(clicks):.1f} (SD={np.std(clicks):.1f})")
    print(f"  Events logged: M={np.mean(n_events):.1f} (SD={np.std(n_events):.1f})")
    print(f"  Predictions viewed: M={np.mean(predictions):.1f} (SD={np.std(predictions):.1f})")
    print(f"  Recommendations clicked: M={np.mean(recommendations):.1f} (SD={np.std(recommendations):.1f})")\
"""))

# ──────────────────────────────────────────────
# CELL 7 — Dummy data explanation (markdown)
# ──────────────────────────────────────────────
cells.append(mk_md("""\
### Generating Dummy Evaluation Data

In a live evaluation, the CSV files and interaction logs would come from actual participants. For this workshop, we use pre-generated dummy data that simulates realistic responses:

- **Post-test CSVs:** Generated with controlled distributions matching expected patterns
  - SUS scores follow approximately normal distribution (P1: M\u224872, P2: M\u224868)
  - Likert responses include realistic variance and inter-item correlations
  - Open-ended responses are varied and represent common feedback themes
  
- **Interaction logs:** Simulated with realistic:
  - Session durations (15-60 minutes for P1, 10-45 minutes for P2)
  - Event sequences following logical page navigation patterns
  - Feature usage patterns matching expected prototype exploration
  - Error occurrences at realistic low rates

- **Qualitative coded data:** Pre-coded with dual-coder simulation
  - Two "LLM coders" independently assigned codes
  - ~83-85% inter-coder agreement (realistic for open coding)
  - Enables computing inter-rater reliability in Section 6

> **Validity Note:** While dummy data allows demonstrating the full pipeline, all statistical results should be interpreted as illustrative only. In a real study, actual participant data would replace these files at this step."""))


# ──────────────────────────────────────────────
# Write JSON
# ──────────────────────────────────────────────
output_path = "/home/user/empty3/notebook_part2.json"
with open(output_path, "w", encoding="utf-8") as fout:
    json.dump(cells, fout, indent=1, ensure_ascii=False)

print(f"Wrote {len(cells)} cells to {output_path}")
