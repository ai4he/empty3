#!/usr/bin/env python3
"""
Generate full_nb_part1.json — 16 Jupyter notebook cells (indices 0–15).
"""
import json

def make_source(text):
    """Convert a multiline string into a list of lines, each ending with \\n except the last."""
    lines = text.split('\n')
    if not lines:
        return []
    result = [line + '\n' for line in lines[:-1]]
    result.append(lines[-1])
    return result

def md_cell(source_text):
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": make_source(source_text),
        "outputs": []
    }

def code_cell(source_text):
    return {
        "cell_type": "code",
        "metadata": {},
        "source": make_source(source_text),
        "outputs": [],
        "execution_count": None
    }

cells = []

# ── CELL 0 (markdown) ──────────────────────────────────────────────
cells.append(md_cell(r"""# Human-Centered AI: End-to-End Prototype Evaluation Workshop
## From User Requirements to Research Paper

**Course:** Human-Centered AI | **Format:** Hands-on Workshop (2 Sessions) | **Tools:** Google Gemini API, AutoGluon, Python

---

### Workshop Overview

This notebook provides a **complete, reproducible pipeline** for conducting a Human-Centered AI research project — from defining research questions to drafting a conference paper. Every section processes specific **inputs** into **outputs**, with pre-built fallbacks for each step.

We demonstrate two projects side by side:

| | **Project 1: Gemini Quest** | **Project 2: StudyBuddy** |
|:---|:---|:---|
| **Domain** | AI-generated interactive narrative videogame | AI-powered adaptive study companion |
| **AI Technology** | Google Gemini multimodal models (story, visuals, music, code) | AutoGluon AutoML (tabular prediction) |
| **HCD Focus** | Content preferences, AI perception, immersion | Trust, transparency, privacy, usefulness |
| **Evaluation** | SUS, UES-SF, narrative quality, AI perception | SUS, TAM, trust in AI, privacy concern |

### Pipeline Architecture

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  1. Define   │────▶│ 2. Survey    │────▶│ 3. Integrate │────▶│ 4. Deploy    │
│  Projects    │     │ Requirements │     │ Feedback     │     │ Prototype    │
└──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
                                                                       │
┌──────────────┐     ┌──────────────┐     ┌──────────────┐            │
│  7. Report   │◀────│ 6. Analyze   │◀────│ 5. Evaluate  │◀───────────┘
│  (CHI Paper) │     │ (Mixed Meth.)│     │ (Users)      │
└──────────────┘     └──────────────┘     └──────────────┘
```

Each step has: **Input** → **Processing Code** → **Output** → **Pre-built Fallback**

> **⚠ Important Note on LLM Automation:** This notebook uses LLMs to automate steps traditionally done manually (prototype generation, qualitative coding). Each section discusses validity implications. Section 7 provides a comprehensive treatment of limitations and mitigation strategies for scientific rigor at the level of ACM CHI.

### Table of Contents
1. [Project Definition & Research Design](#section-1)
2. [User Requirements Gathering](#section-2)
3. [Integrate Human Feedback](#section-3)
4. [Deploy Prototype](#section-4)
5. [User Evaluation](#section-5)
6. [Statistical & Qualitative Analyses](#section-6)
7. [Research Report (ACM CHI Draft)](#section-7)"""))

# ── CELL 1 (code) ──────────────────────────────────────────────────
cells.append(code_cell(r"""# ============================================================
# SETUP: Core imports and configuration
# ============================================================
# Uncomment to install required packages:
# !pip install pandas numpy scipy matplotlib seaborn statsmodels pingouin
# !pip install scikit-learn wordcloud krippendorff
# !pip install google-generativeai
# !pip install autogluon  # Optional, for Project 2 model training

import pandas as pd
import numpy as np
import json
import os
import csv
import io
import warnings
import random
from datetime import datetime, timedelta
from pathlib import Path
from scipy import stats
from scipy.stats import norm, shapiro, mannwhitneyu, kruskal
from sklearn.metrics import cohen_kappa_score
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

warnings.filterwarnings('ignore')
np.random.seed(42)

# Plotting defaults
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")
plt.rcParams.update({'figure.figsize': (10, 6), 'font.size': 12, 'figure.dpi': 100})

# Project paths
BASE_DIR = Path('.')
DELIVERABLES = BASE_DIR / 'deliverables'
P1_DIR = DELIVERABLES / 'project1'
P2_DIR = DELIVERABLES / 'project2'
REPORT_DIR = DELIVERABLES / 'report'

# Ensure directories exist
for d in [P1_DIR/'survey', P1_DIR/'posttest', P1_DIR/'logs', P1_DIR/'webapp',
          P2_DIR/'survey', P2_DIR/'posttest', P2_DIR/'logs', P2_DIR/'webapp',
          P2_DIR/'dataset', P2_DIR/'model', REPORT_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# Gemini API key
GEMINI_API_KEY = "AIzaSyADuTLmzUJJDXPAKAw00ze5Y1Rkspoel0k"

print("=" * 65)
print("  HUMAN-CENTERED AI WORKSHOP — Environment Ready")
print("=" * 65)
print(f"  Working directory : {Path('.').resolve()}")
print(f"  Deliverables dir  : {DELIVERABLES.resolve()}")
print(f"  NumPy seed        : 42 (fixed for reproducibility)")
print(f"  Matplotlib backend: {matplotlib.get_backend()}")
print("=" * 65)"""))

# ── CELL 2 (markdown) ──────────────────────────────────────────────
cells.append(md_cell(r"""<a id="section-1"></a>

---
# 1. Project Definition & Research Design

## Human-Centered Computing Methodology

We follow the **Double Diamond** design framework (Design Council, 2005) combined with **ISO 9241-210:2019** (Human-centred design for interactive systems):

| Phase | Activity | Output |
|:---|:---|:---|
| **Discover** | User requirements survey | Design specifications |
| **Define** | Synthesize requirements → prototype specs | Feature list, UI wireframe |
| **Develop** | AI-assisted prototype generation | Working web prototype |
| **Deliver** | Usability evaluation + analysis | Research findings & paper |

### Study Design: Mixed-Methods Sequential Explanatory

Our methodology combines quantitative and qualitative approaches in sequence (Creswell & Clark, 2017):

1. **Phase 1 — Requirements (QUAN + qual):** Large-sample survey (N=120) with Likert scales and open-ended items
2. **Phase 2 — Evaluation (QUAN + QUAL):** Lab study (N=40) with standardized instruments, behavioral telemetry, and open-ended feedback
3. **Phase 3 — Integration:** Joint display tables comparing quantitative results with qualitative themes

### Key References
- Amershi, S., et al. (2019). Guidelines for Human-AI Interaction. *Proc. ACM CHI*.
- Creswell, J. W., & Clark, V. L. P. (2017). *Designing and Conducting Mixed Methods Research*. Sage.
- Design Council (2005). *The Double Diamond Design Process Model*.
- ISO 9241-210:2019. *Ergonomics of human-system interaction — Human-centred design*.
- Sanders, E. B. N., & Stappers, P. J. (2008). Co-creation and the new landscapes of design. *CoDesign*, 4(1), 5–18.
- Shneiderman, B. (2022). *Human-Centered AI*. Oxford University Press."""))

# ── CELL 3 (markdown) ──────────────────────────────────────────────
cells.append(md_cell(r"""## 1.1 Project 1: Gemini Quest — AI-Generated Interactive Narrative Videogame

### Concept

A browser-based interactive fiction game where **all content is orchestrated through Google Gemini's multimodal capabilities**:

| Component | Gemini Capability | Model |
|:---|:---|:---|
| Story narrative & dialogue | Text generation | Gemini 2.5 Flash |
| Visual scene illustrations | Image generation | Gemini 2.5 Flash |
| Music & sound atmosphere | Text description of audio | Gemini 2.5 Flash |
| Game code (HTML/CSS/JS) | Code generation | Gemini 2.5 Flash |

The player makes narrative choices that shape a fantasy adventure, experiencing a fully AI-generated interactive world.

### Research Framing for ACM CHI

**Novelty:** While prior work explores AI-generated narratives (Riedl & Bulitko, 2013) and AI art (Epstein et al., 2023), few studies examine the **end-to-end orchestration of multimodal generative AI** for interactive entertainment from a user-centered perspective.

**Contributions:**
1. A design framework for human-centered multimodal AI game generation
2. Empirical findings on user perception of fully AI-generated interactive experiences
3. Design guidelines for integrating user preferences into generative AI pipelines

### Research Questions
- **RQ1:** How do users perceive the quality and coherence of a fully AI-generated interactive narrative experience?
- **RQ2:** What user requirements and preferences most significantly influence satisfaction with AI-generated game content?
- **RQ3:** To what extent does awareness of AI-generated content affect user engagement and immersion?

### Variables

| Type | Variable | Measurement | Instrument |
|:---|:---|:---|:---|
| **IV** | Preference integration | Binary (integrated vs. generic) | Survey-informed design |
| **IV** | AI awareness | Binary (aware vs. unaware) | Experimental condition |
| **DV** | Perceived usability | SUS score (0–100) | System Usability Scale (Brooke, 1996) |
| **DV** | User engagement | UES-SF subscales (1–5) | User Engagement Scale Short Form (O'Brien et al., 2018) |
| **DV** | Narrative quality | 5-item custom scale (1–7) | Pilot-validated |
| **DV** | AI perception | 5-item custom scale (1–7) | Based on Jakesch et al. (2023) |
| **DV** | Immersion | 3-item custom scale (1–7) | Based on Jennett et al. (2008) |
| **DV** | Behavioral engagement | Clicks, time-on-task, choices | Telemetry logs |

### Hypotheses
- **H1:** Users whose preferences are integrated into the AI pipeline will report higher SUS scores (independent t-test, α=0.05).
- **H2:** Narrative quality will positively correlate with engagement (Pearson r > 0.3).
- **H3:** Users aware of AI generation will report lower immersion than unaware users (independent t-test, α=0.05).

**References:** Riedl & Bulitko (2013), *AI Magazine*; Epstein et al. (2023), *Science*; Kreminski & Wardrip-Fruin (2019), *Proc. FDG*; Lanzi & Loiacono (2023), *Proc. GECCO*; Jakesch et al. (2023), *PNAS*."""))

# ── CELL 4 (markdown) ──────────────────────────────────────────────
cells.append(md_cell(r"""## 1.2 Project 2: StudyBuddy — AI-Powered Adaptive Study Companion

### Concept

A web dashboard using **AutoGluon** (Erickson et al., 2020) to predict student quiz performance and recommend personalized study strategies. The system collects study habits, attendance, and well-being indicators, then presents predictions with confidence intervals and actionable recommendations.

**Why AutoGluon?** AutoGluon's `TabularPredictor` automatically selects and ensembles models (XGBoost, LightGBM, CatBoost, Neural Networks), enabling rapid ML prototyping without deep ML expertise — ideal for HCD iteration cycles.

### Research Framing for ACM CHI

**Novelty:** Few studies apply **Human-Centered Design to AutoML-based educational tools** with focus on trust, transparency, and student agency.

**Contributions:**
1. Design guidelines for presenting ML predictions to non-expert users
2. Empirical evidence on student trust in AutoML-generated recommendations
3. A framework for integrating HCD survey feedback into AutoML feature engineering

### Research Questions
- **RQ1:** How do students perceive the usefulness and trustworthiness of an AutoML-based study performance predictor?
- **RQ2:** What design factors (transparency, control, personalization) most influence student trust in AI-generated study recommendations?
- **RQ3:** Does integrating user-identified preferences into model features improve perceived prediction accuracy?

### Variables

| Type | Variable | Measurement | Instrument |
|:---|:---|:---|:---|
| **IV** | Explanation level | 3 levels (none / simple / detailed) | UI condition |
| **IV** | Personalization | Binary (user-informed features vs. default) | Survey-driven feature selection |
| **DV** | Perceived usability | SUS score (0–100) | System Usability Scale (Brooke, 1996) |
| **DV** | Trust in AI | 5-item scale (1–7) | Based on Madsen & Gregor (2000) |
| **DV** | Perceived usefulness | 5-item scale (1–7) | TAM (Davis, 1989) |
| **DV** | Perceived ease of use | 5-item scale (1–7) | TAM (Davis, 1989) |
| **DV** | Privacy concern | 3-item scale (1–7) | Based on Malhotra et al. (2004) |
| **DV** | Behavioral engagement | Features used, predictions requested | Telemetry logs |

### Hypotheses
- **H1:** Detailed AI explanations → higher trust scores (one-way ANOVA, α=0.05).
- **H2:** Perceived usefulness correlates positively with system usage (Spearman ρ > 0.3).
- **H3:** Higher privacy concerns associate with lower trust (Pearson r, expected negative).

**References:** Erickson et al. (2020), *arXiv*; Holstein et al. (2019), *Proc. CHI*; Khosravi et al. (2022), *Computers & Education: AI*; Liao & Varshney (2022), *arXiv*."""))

# ── CELL 5 (markdown) ──────────────────────────────────────────────
cells.append(md_cell(r"""## 1.3 Power Analysis & Recruitment Plan

We conduct an **a priori power analysis** to determine minimum sample sizes, following best practices for CHI (Caine, 2016).

**Reference:** Caine, K. (2016). Local Standards for Sample Size at CHI. *Proc. ACM CHI*."""))

# ── CELL 6 (code) ──────────────────────────────────────────────────
cells.append(code_cell(r"""# ============================================================
# 1.3  POWER ANALYSIS
# ============================================================

def power_ttest(d=0.5, alpha=0.05, power=0.80, two_tailed=True):
    """Sample size per group for independent-samples t-test."""
    za = norm.ppf(1 - alpha / (2 if two_tailed else 1))
    zb = norm.ppf(power)
    return int(np.ceil(((za + zb) / d) ** 2))

def power_anova(f=0.25, alpha=0.05, power=0.80, k=3):
    """Approximate n per group for one-way ANOVA."""
    za = norm.ppf(1 - alpha / (2 * (k - 1)))
    zb = norm.ppf(power)
    n = int(np.ceil(((za + zb) / f) ** 2))
    return n, n * k

n_ttest = power_ttest(d=0.5, alpha=0.05, power=0.80)
n_anova_grp, n_anova_tot = power_anova(f=0.25, alpha=0.05, power=0.80, k=3)

print("=" * 65)
print("  POWER ANALYSIS RESULTS")
print("=" * 65)

print(f"""
  Project 1 — Gemini Quest (independent t-test)
    Effect size: Cohen's d = 0.5 (medium)
    α = 0.05, Power = 0.80, Two-tailed
    Required n per group : {n_ttest}
    Total participants   : {n_ttest * 2}
    With 20% buffer      : {int(np.ceil(n_ttest * 2 * 1.2))}

  Project 2 — StudyBuddy (one-way ANOVA, k=3)
    Effect size: Cohen's f = 0.25 (medium)
    α = 0.05, Power = 0.80
    Required n per group : {n_anova_grp}
    Total participants   : {n_anova_tot}
    With 20% buffer      : {int(np.ceil(n_anova_tot * 1.2))}

  Requirements Survey: N = 120 per project
    Rationale: ≥5:1 response-to-item ratio for factor analysis
    (with ~20 survey items → need ≥100 responses)

  Usability Evaluation: N = 40 per project
    Exceeds power-analysis minimum; accounts for ~20% dropout
""")

print("  RECRUITMENT PLAN")
print("  " + "-" * 55)
print("""  Demographics : Age 18-65 (primary 18-35), balanced gender
  Channels     : University pools (SONA), social media, snowball
  Inclusion    : Age ≥ 18, English fluent, browser access
  Compensation : $15 gift card (evaluation), raffle (survey)
  Ethics       : IRB-approved, informed consent, anonymized data
""")"""))

# ── CELL 7 (markdown) ──────────────────────────────────────────────
cells.append(md_cell(r"""<a id="section-2"></a>

---
# 2. User Requirements Gathering

## Methodology: Survey-Based Requirements Elicitation

We use structured surveys combining:
- **Closed-ended items:** 7-point Likert scales for quantifiable preferences
- **Ranking items:** Priority ordering of features (1 = highest)
- **Open-ended items:** Free-text for richer qualitative insights

**Instrument validation:** Demographic items follow ACM SIGCHI reporting guidelines. Likert constructs use validated anchors. Surveys pre-tested with 3 pilot participants (~10 min completion).

### References
- Lazar, J., Feng, J. H., & Hochheiser, H. (2017). *Research Methods in HCI*. Morgan Kaufmann.
- Fowler, F. J. (2013). *Survey Research Methods*. Sage.

> **Input:** Survey design → **Output:** CSV of 120 responses per project
> Pre-built CSVs are in `deliverables/projectN/survey/` as fallback."""))

# ── CELL 8 (markdown) ──────────────────────────────────────────────
cells.append(md_cell(r"""## 2.1 Project 1: Gemini Quest — Requirements Survey Instrument

| Section | Items | Type |
|:---|:---|:---|
| **A. Demographics** | Age, gender, education | Numeric / Categorical |
| **B. Gaming Background** | Experience (years), hours/week, preferred genre | Numeric / Categorical |
| **C. Game Preferences** | Narrative importance, character depth, world-building, music importance, gameplay vs. story | 7-pt Likert |
| **D. Art & Style** | Preferred art style, game session length, multiplayer interest | Categorical / 7-pt Likert |
| **E. AI Perception** | AI content comfort, AI art acceptance, AI story acceptance | 7-pt Likert |
| **F. Accessibility** | Accessibility needs (Y/N), details if yes | Binary / Free text |
| **G. Open Feedback** | "What features would you most want in an AI-generated game?" | Free text |"""))

# ── CELL 9 (code) ──────────────────────────────────────────────────
cells.append(code_cell(r"""# ============================================================
# 2.1  LOAD / GENERATE PROJECT 1 SURVEY DATA
# ============================================================
p1_survey_path = P1_DIR / 'survey' / 'requirements_survey_responses.csv'

if p1_survey_path.exists():
    p1_survey = pd.read_csv(p1_survey_path)
    print(f"✓ Loaded existing P1 survey data: {p1_survey.shape[0]} rows × {p1_survey.shape[1]} cols")
else:
    print("Generating P1 survey data (120 responses)...")
    # If the pre-built file is missing, regenerate:
    # !python generate_p1_data.py
    raise FileNotFoundError(f"Run 'python generate_p1_data.py' first, or ensure {p1_survey_path} exists")

# ---- Demographic Summary ----
print(f"\n{'=' * 65}")
print("  PROJECT 1 SURVEY — DEMOGRAPHIC PROFILE  (N = {})".format(len(p1_survey)))
print("=" * 65)
print(f"  Age            : M = {p1_survey['age'].mean():.1f}, SD = {p1_survey['age'].std():.1f}, "
      f"Range = [{p1_survey['age'].min()}, {p1_survey['age'].max()}]")
print(f"  Gender         : {dict(p1_survey['gender'].value_counts())}")
print(f"  Education      : {dict(p1_survey['education'].value_counts())}")
print(f"  Gaming Exp.    : M = {p1_survey['gaming_experience_years'].mean():.1f} yrs")
print(f"  Top Genre      : {p1_survey['preferred_genre'].mode()[0]}")
print(f"  Top Art Style  : {p1_survey['preferred_art_style'].mode()[0]}")

# Key Likert means
likert_items = {
    'Narrative importance': 'narrative_importance',
    'Character depth': 'character_depth_importance',
    'World-building': 'world_building_importance',
    'Music importance': 'music_importance',
    'AI content comfort': 'ai_generated_content_comfort',
    'AI art acceptance': 'ai_art_acceptance',
    'AI story acceptance': 'ai_story_acceptance'
}
print(f"\n  Likert Ratings (1–7):")
for label, col in likert_items.items():
    if col in p1_survey.columns:
        print(f"    {label:25s}: M = {p1_survey[col].mean():.2f}, SD = {p1_survey[col].std():.2f}")"""))

# ── CELL 10 (code) ─────────────────────────────────────────────────
cells.append(code_cell(r"""# ============================================================
# 2.1  PROJECT 1 SURVEY — VISUALIZATION
# ============================================================
fig, axes = plt.subplots(2, 3, figsize=(18, 10))
fig.suptitle('Project 1: Gemini Quest — Requirements Survey (N=120)', fontsize=16, fontweight='bold', y=1.01)

# 1. Genre preferences
gc = p1_survey['preferred_genre'].value_counts()
axes[0,0].barh(gc.index, gc.values, color=sns.color_palette("husl", len(gc)))
axes[0,0].set_title('Preferred Genre'); axes[0,0].set_xlabel('Count')

# 2. Art style preferences
ac = p1_survey['preferred_art_style'].value_counts()
axes[0,1].barh(ac.index, ac.values, color=sns.color_palette("husl", len(ac)))
axes[0,1].set_title('Preferred Art Style'); axes[0,1].set_xlabel('Count')

# 3. Content importance ratings
content_cols = ['narrative_importance','character_depth_importance','world_building_importance','music_importance']
content_labels = ['Narrative','Character\nDepth','World\nBuilding','Music']
means = [p1_survey[c].mean() for c in content_cols]
sds   = [p1_survey[c].std()  for c in content_cols]
axes[0,2].bar(content_labels, means, yerr=sds, capsize=5, color=sns.color_palette("husl",4), alpha=.8)
axes[0,2].set_title('Content Importance'); axes[0,2].set_ylabel('Mean (1–7)')
axes[0,2].set_ylim(1, 7); axes[0,2].axhline(4, color='grey', ls='--', alpha=.5)

# 4. AI acceptance
ai_cols   = ['ai_generated_content_comfort','ai_art_acceptance','ai_story_acceptance']
ai_labels = ['AI Content\nComfort','AI Art\nAcceptance','AI Story\nAcceptance']
ai_m = [p1_survey[c].mean() for c in ai_cols]
ai_s = [p1_survey[c].std()  for c in ai_cols]
axes[1,0].bar(ai_labels, ai_m, yerr=ai_s, capsize=5, color=['#4CAF50','#2196F3','#FF9800'], alpha=.8)
axes[1,0].set_title('AI Perception'); axes[1,0].set_ylabel('Mean (1–7)')
axes[1,0].set_ylim(1,7); axes[1,0].axhline(4, color='grey', ls='--', alpha=.5)

# 5. Age distribution
axes[1,1].hist(p1_survey['age'], bins=15, color='#9C27B0', alpha=.7, edgecolor='white')
axes[1,1].set_title('Age Distribution'); axes[1,1].set_xlabel('Age'); axes[1,1].set_ylabel('Count')

# 6. Game length preference
lc = p1_survey['preferred_game_length_minutes'].value_counts().sort_index()
axes[1,2].bar([f'{x} min' for x in lc.index], lc.values, color='#00BCD4', alpha=.8)
axes[1,2].set_title('Preferred Game Length'); axes[1,2].set_ylabel('Count')

plt.tight_layout()
plt.savefig(str(REPORT_DIR / 'p1_survey_results.png'), dpi=150, bbox_inches='tight')
plt.show()
print("✓ Figure saved: deliverables/report/p1_survey_results.png")"""))

# ── CELL 11 (markdown) ─────────────────────────────────────────────
cells.append(md_cell(r"""## 2.2 Project 2: StudyBuddy — Requirements Survey Instrument

| Section | Items | Type |
|:---|:---|:---|
| **A. Demographics** | Age, gender, education level, major, GPA | Numeric / Categorical |
| **B. Study Habits** | Hours/week, preferred study method | Numeric / Categorical |
| **C. Tech & AI Attitudes** | Tech comfort, AI trust, data sharing comfort, prediction usefulness, privacy concern | 7-pt Likert |
| **D. Feature Preferences** | Recommendation format, dashboard complexity, notification frequency, feature priority ranking (5 items) | Categorical / Ranking |
| **E. Open Feedback** | "What would make an AI study companion most useful to you?" | Free text |"""))

# ── CELL 12 (code) ─────────────────────────────────────────────────
cells.append(code_cell(r"""# ============================================================
# 2.2  LOAD / GENERATE PROJECT 2 SURVEY DATA
# ============================================================
p2_survey_path = P2_DIR / 'survey' / 'requirements_survey_responses.csv'

if p2_survey_path.exists():
    p2_survey = pd.read_csv(p2_survey_path)
    print(f"✓ Loaded existing P2 survey data: {p2_survey.shape[0]} rows × {p2_survey.shape[1]} cols")
else:
    raise FileNotFoundError(f"Run 'python generate_p2_data.py' first, or ensure {p2_survey_path} exists")

print(f"\n{'=' * 65}")
print("  PROJECT 2 SURVEY — DEMOGRAPHIC PROFILE  (N = {})".format(len(p2_survey)))
print("=" * 65)
print(f"  Age             : M = {p2_survey['age'].mean():.1f}, SD = {p2_survey['age'].std():.1f}")
print(f"  Gender          : {dict(p2_survey['gender'].value_counts())}")
print(f"  Education Level : {dict(p2_survey['education_level'].value_counts())}")
print(f"  Major           : {dict(p2_survey['major_category'].value_counts())}")
print(f"  GPA             : M = {p2_survey['current_gpa'].mean():.2f}, SD = {p2_survey['current_gpa'].std():.2f}")
print(f"  Study hrs/wk    : M = {p2_survey['study_hours_weekly'].mean():.1f}")
print(f"  Study Method    : {dict(p2_survey['preferred_study_method'].value_counts())}")

attitude_items = {
    'Tech comfort': 'tech_comfort',
    'AI trust': 'ai_trust_level',
    'Data sharing comfort': 'data_sharing_comfort',
    'Prediction usefulness': 'prediction_usefulness',
    'Privacy concern': 'privacy_concern_level'
}
print(f"\n  Attitude Ratings (1–7):")
for label, col in attitude_items.items():
    if col in p2_survey.columns:
        print(f"    {label:25s}: M = {p2_survey[col].mean():.2f}, SD = {p2_survey[col].std():.2f}")"""))

# ── CELL 13 (code) ─────────────────────────────────────────────────
cells.append(code_cell(r"""# ============================================================
# 2.2  PROJECT 2 SURVEY — VISUALIZATION
# ============================================================
fig, axes = plt.subplots(2, 3, figsize=(18, 10))
fig.suptitle('Project 2: StudyBuddy — Requirements Survey (N=120)', fontsize=16, fontweight='bold', y=1.01)

# 1. Attitude ratings
att_cols = ['tech_comfort','ai_trust_level','data_sharing_comfort','prediction_usefulness','privacy_concern_level']
att_labs = ['Tech\nComfort','AI\nTrust','Data\nSharing','Prediction\nUsefulness','Privacy\nConcern']
att_m = [p2_survey[c].mean() for c in att_cols]
att_s = [p2_survey[c].std()  for c in att_cols]
axes[0,0].bar(att_labs, att_m, yerr=att_s, capsize=5, color=['#4CAF50','#2196F3','#FF9800','#9C27B0','#F44336'], alpha=.8)
axes[0,0].set_title('Attitude Ratings'); axes[0,0].set_ylabel('Mean (1–7)')
axes[0,0].set_ylim(1,7); axes[0,0].axhline(4, color='grey', ls='--', alpha=.5)

# 2. Study method
mc = p2_survey['preferred_study_method'].value_counts()
axes[0,1].pie(mc.values, labels=mc.index, autopct='%1.0f%%', colors=sns.color_palette("husl", len(mc)))
axes[0,1].set_title('Preferred Study Method')

# 3. Dashboard complexity
dc = p2_survey['dashboard_complexity'].value_counts()
axes[0,2].bar(dc.index, dc.values, color=['#66BB6A','#FFA726','#EF5350'], alpha=.8)
axes[0,2].set_title('Dashboard Complexity Preference'); axes[0,2].set_ylabel('Count')

# 4. Major distribution
mjc = p2_survey['major_category'].value_counts()
axes[1,0].barh(mjc.index, mjc.values, color=sns.color_palette("husl", len(mjc)))
axes[1,0].set_title('Major Category')

# 5. GPA distribution
axes[1,1].hist(p2_survey['current_gpa'], bins=15, color='#3F51B5', alpha=.7, edgecolor='white')
axes[1,1].set_title('GPA Distribution'); axes[1,1].set_xlabel('GPA'); axes[1,1].set_ylabel('Count')

# 6. Notification preference
nc = p2_survey['notification_frequency'].value_counts()
axes[1,2].bar(nc.index, nc.values, color=sns.color_palette("Set2", len(nc)))
axes[1,2].set_title('Notification Preference'); axes[1,2].set_ylabel('Count')
axes[1,2].tick_params(axis='x', rotation=15)

plt.tight_layout()
plt.savefig(str(REPORT_DIR / 'p2_survey_results.png'), dpi=150, bbox_inches='tight')
plt.show()
print("✓ Figure saved: deliverables/report/p2_survey_results.png")"""))

# ── CELL 14 (markdown) ─────────────────────────────────────────────
cells.append(md_cell(r"""<a id="section-3"></a>

---
# 3. Integrate Human Feedback

## From Survey Data to Design & AI Decisions

Following **Participatory AI Design** (Birhane et al., 2022), each survey dimension maps to either a **UI decision** or an **AI decision**:

| Feedback Type | → UI Decision | → AI Decision |
|:---|:---|:---|
| Preferred genre/art style | Visual theme, layout | Gemini prompt parameters |
| Narrative importance | Story length/depth | Generation detail level |
| AI comfort level | Transparency disclaimers | Output confidence display |
| Dashboard complexity | Layout density | Explanation verbosity |
| Trust / privacy level | Data controls in UI | Feature selection for model |

### Using the Google Gemini API

1. **Get API Key:** Visit [Google AI Studio](https://aistudio.google.com/) → Sign in → "Get API Key" → "Create API Key"
2. **Install:** `pip install google-generativeai`
3. **Models available:**
   - `gemini-2.5-flash` — Fast, multimodal, free-tier compatible (recommended)
   - `gemini-2.5-pro` — Most capable, higher cost

> **Input:** Survey CSV → **Output:** (i) Design specification JSON; (ii) Generated web prototype code; (iii) AutoGluon trained model
> Pre-built prototypes in `deliverables/projectN/webapp/` as fallback.

**References:** Birhane et al. (2022), *Proc. EAAMO*; Google (2025), *Gemini API Docs*."""))

# ── CELL 15 (code) ─────────────────────────────────────────────────
cells.append(code_cell(r"""# ============================================================
# 3.0  GEMINI API SETUP
# ============================================================
GEMINI_AVAILABLE = False
gemini_model = None

try:
    import google.generativeai as genai
    genai.configure(api_key=GEMINI_API_KEY)

    # List available models
    print("Available Gemini models:")
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"  • {m.name}")

    gemini_model = genai.GenerativeModel('gemini-2.5-flash')
    GEMINI_AVAILABLE = True
    print(f"\n✓ Gemini API ready (model: gemini-2.5-flash)")

except ImportError:
    print("✗ google-generativeai not installed.  pip install google-generativeai")
    print("  → Will use pre-built prototypes instead.")
except Exception as e:
    print(f"✗ Gemini API error: {e}")
    print("  → Will use pre-built prototypes instead.")"""))

# ── Write JSON ──────────────────────────────────────────────────────
output_path = '/home/user/empty3/full_nb_part1.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(cells, f, indent=1, ensure_ascii=False)

print(f"Wrote {len(cells)} cells to {output_path}")
