#!/usr/bin/env python3
"""
Generate all dummy data for Project 1: Gemini Quest - AI-Generated Interactive Narrative Videogame.

Produces:
  1. Requirements survey CSV (120 responses)
  2. Post-test survey CSV (40 responses)
  3. Interaction logs JSON (40 participants)
  4. Coded qualitative data CSV

Uses numpy seed 42 for reproducibility.
"""

import csv
import json
import os
import random
from datetime import datetime, timedelta

import numpy as np

# ---------------------------------------------------------------------------
# Reproducibility
# ---------------------------------------------------------------------------
np.random.seed(42)
random.seed(42)

# ---------------------------------------------------------------------------
# Output paths
# ---------------------------------------------------------------------------
SURVEY_PATH = "/home/user/empty3/deliverables/project1/survey/requirements_survey_responses.csv"
POSTTEST_PATH = "/home/user/empty3/deliverables/project1/posttest/posttest_survey_responses.csv"
LOGS_PATH = "/home/user/empty3/deliverables/project1/logs/interaction_logs.json"
CODED_PATH = "/home/user/empty3/deliverables/project1/posttest/coded_qualitative_data.csv"

for p in [SURVEY_PATH, POSTTEST_PATH, LOGS_PATH, CODED_PATH]:
    os.makedirs(os.path.dirname(p), exist_ok=True)

# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def likert(low, high, mean, std, size=1):
    """Return integer Likert-scale values clipped to [low, high]."""
    vals = np.round(np.random.normal(mean, std, size)).astype(int)
    return np.clip(vals, low, high)


def weighted_choice(options, weights, size=1):
    """Weighted random choice returning a list of strings."""
    p = np.array(weights, dtype=float)
    p /= p.sum()
    return list(np.random.choice(options, size=size, p=p))


# ---------------------------------------------------------------------------
# Open-ended text banks
# ---------------------------------------------------------------------------

OPEN_FEEDBACK_POSITIVE = [
    "I think AI-generated stories could be really exciting if they adapt to player choices in meaningful ways and keep the narrative fresh every playthrough.",
    "Would love to see an AI game that creates unique storylines each time. The replayability factor alone would be incredible for narrative-driven experiences.",
    "AI art in games has gotten impressively good. I would enjoy a game where environments shift based on mood and story beats, creating a personalized atmosphere.",
    "The concept of AI-generated narratives is fascinating. If the writing quality is high enough, I could see myself spending hours exploring branching paths.",
    "I am excited about AI games because they could solve the problem of repetitive content. Every session could feel genuinely new and surprising.",
    "If AI can generate characters with real emotional depth, that would be a game-changer. I want to feel connected to the story, not just clicking through text.",
    "I hope AI-generated games focus on atmosphere and world-building. A rich, immersive setting is what keeps me playing more than anything else.",
    "The potential for AI to create adaptive difficulty and story pacing is what interests me most. Games that respond to how I play are the future.",
    "I would be thrilled to play an AI narrative game with beautiful procedural art and a soundtrack that changes with the story. Total immersion is the goal.",
    "AI storytelling could finally deliver on the promise of truly open-ended RPGs where your choices actually matter and the world remembers everything.",
    "What excites me is the possibility of AI creating side quests and lore that feel hand-crafted. If done well, it could rival traditionally written games.",
    "I want an AI game that surprises me. Not random surprises, but narratively coherent twists that feel like they were planned just for my playthrough.",
    "AI-generated content could make indie games compete with AAA titles in terms of content volume. That democratization of game development is exciting.",
    "If the AI can maintain consistent character personalities throughout the story while still allowing growth and change, I am fully on board.",
    "The idea of an AI dungeon master that crafts encounters based on my party composition and past decisions sounds like the perfect tabletop-to-digital translation.",
]

OPEN_FEEDBACK_SKEPTICAL = [
    "I am a bit skeptical about AI-generated narratives. Most AI text I have read feels generic and lacks the nuance of human writers. Prove me wrong.",
    "My concern with AI games is consistency. AI often contradicts itself in longer narratives, and that breaks immersion faster than anything else.",
    "I worry AI-generated content will feel soulless. Games are art, and I am not sure algorithms can capture the human touch that makes stories resonate.",
    "AI art and writing still have a long way to go. I have seen too many AI artifacts and nonsensical plot points to fully trust the technology yet.",
    "While the concept is interesting, I fear AI games will become a crutch for lazy developers who skip proper quality assurance and narrative design.",
    "I need to see proof that AI narratives can handle complex themes like morality and loss with the subtlety they deserve before I commit to playing.",
    "The biggest risk with AI content is repetitive patterns. AI models tend to fall into predictable structures, and experienced gamers will notice quickly.",
    "I am cautiously interested but worried about the uncanny valley effect in AI writing. Close-to-human but not-quite writing can be more jarring than obviously procedural text.",
    "AI-generated games sound cool in theory, but every demo I have tried felt shallow. I hope this project addresses depth and emotional weight seriously.",
    "My main concern is that AI-generated content often lacks cultural sensitivity and nuance. Games tackle complex topics and AI might oversimplify them.",
]

OPEN_FEEDBACK_MIXED = [
    "I think AI games could work for casual experiences, but for a deep narrative RPG I still prefer human writers. Maybe a hybrid approach would be best.",
    "Interesting concept. I would want strong human oversight on the AI-generated content to ensure quality and coherence throughout the experience.",
    "I could see AI being great for procedural side content while human writers handle the main storyline. Best of both worlds approach seems wise.",
    "The technology is promising but not there yet for full games. I would play this to see how far AI has come, but my expectations are moderate.",
    "I like the idea of AI-generated content for replayability, but I hope there is a solid hand-crafted narrative backbone holding everything together.",
]

POSITIVE_FEEDBACK_POSTTEST = [
    "The narrative branching felt genuinely responsive to my choices. I was impressed by how the story adapted when I made unexpected decisions.",
    "Beautiful art style that maintained consistency throughout. The AI-generated environments had a cohesive aesthetic that really drew me in.",
    "Character dialogue felt surprisingly natural and engaging. I found myself genuinely caring about the outcomes of conversations.",
    "The music adaptation was a standout feature. How it shifted with story beats created an incredibly atmospheric experience.",
    "I loved the character creation system. Being able to influence the AI narrative through my character background was a clever design choice.",
    "The pacing of the story kept me engaged throughout. Each chapter built on the last in a way that felt intentional and well-structured.",
    "World-building was rich and detailed. The lore entries generated for each area added depth without being overwhelming.",
    "The choice system felt meaningful. I could see how my decisions rippled through the narrative in ways both subtle and dramatic.",
    "Really enjoyed the visual storytelling elements. The scene transitions and art composition added emotional weight to key moments.",
    "The game managed to create genuine tension during key story beats. I was genuinely uncertain about outcomes, which is rare in narrative games.",
    "Impressive how the narrative maintained thematic consistency despite being AI-generated. The central themes carried through every chapter.",
    "The puzzle elements integrated naturally into the narrative rather than feeling like arbitrary obstacles. Smart design choice.",
    "I appreciated the accessibility options available. The customizable text size and color settings made the experience comfortable.",
    "The ending felt earned and emotionally satisfying. It tied together threads from earlier choices in a way I did not expect.",
    "Sound design complemented the visuals perfectly. The ambient soundscapes made each location feel alive and unique.",
    "The UI was clean and intuitive. Never once did I feel lost or confused about how to interact with the game.",
    "Dialogue options gave me real agency. I felt like I was shaping the character rather than just selecting from predetermined paths.",
    "The game respected my time. Session length felt right and there were natural stopping points that made it easy to pause and return.",
    "I was surprised by the emotional depth of some scenes. The AI managed to create moments that genuinely moved me.",
    "The variety of narrative paths available adds significant replay value. I immediately wanted to play again making different choices.",
]

NEGATIVE_FEEDBACK_POSTTEST = [
    "Some dialogue transitions felt abrupt, especially when switching between characters. The conversation flow could use more smoothing.",
    "I noticed occasional repetition in descriptive text. Certain phrases appeared multiple times across different scenes.",
    "The AI-generated art had minor inconsistencies in character appearances between scenes. Maintaining visual continuity needs work.",
    "Loading times between chapters were noticeable and broke immersion at critical story moments.",
    "Some narrative branches felt underdeveloped compared to others. The quality was uneven across different choice paths.",
    "The text-heavy sections could benefit from more visual breaks. Long passages without interaction tested my attention span.",
    "Character motivations sometimes felt unclear or contradictory. The AI occasionally lost track of established personality traits.",
    "The final chapter felt rushed compared to the deliberate pacing of earlier sections. More time for resolution would help.",
    "I encountered a visual glitch where background art overlapped dialogue boxes during one scene in chapter two.",
    "The ambient music occasionally looped noticeably, which slightly diminished the otherwise strong atmosphere.",
    "Some choice options felt too similar to each other. I wanted more dramatically different paths to explore.",
    "The settings menu was hard to find during gameplay. An in-game overlay would be more accessible than the current approach.",
    "Certain AI-generated descriptions were overly verbose. Tighter editing would improve readability and pacing.",
    "The difficulty curve for puzzle elements was inconsistent. Some were trivially easy while others halted progress.",
    "I felt the character creation options could be expanded. More background choices would add to the personalization.",
    "Text rendering on some art backgrounds made readability challenging. Better contrast or text boxes would help.",
    "The help system was not very helpful for understanding game mechanics. More contextual tutorials would be welcome.",
    "Some emotional scenes lacked impact because the AI writing was too clinical and detached in tone.",
    "Navigation between previously visited areas was cumbersome. A quick-travel or chapter select would improve the experience.",
    "The game did not clearly indicate when choices were irreversible, which led to some frustrating moments.",
]

SUGGESTIONS_POSTTEST = [
    "Add a journal or codex feature that tracks story decisions and lore entries for reference.",
    "Consider adding voice acting or text-to-speech for key dialogue moments.",
    "A chapter select for replaying with different choices would increase replay value significantly.",
    "Include more visual customization options for the main character during creation.",
    "Add difficulty settings that affect puzzle complexity and narrative branching depth.",
    "Consider implementing a relationship tracker showing how NPCs feel about the player.",
    "A save system with multiple slots would let players explore different narrative branches.",
    "Add optional side stories that expand on secondary characters and world lore.",
    "Include a gallery mode to revisit AI-generated art from completed scenes.",
    "Consider adding collaborative or shared narrative modes for multiplayer experiences.",
    "Implement a feedback button during gameplay so players can flag AI inconsistencies in real time.",
    "Add a narrative recap at the start of each chapter summarizing previous events and choices.",
    "Consider accessibility features like dyslexia-friendly font options and high contrast modes.",
    "A mood or tone selector at the start could help the AI tailor the narrative atmosphere.",
    "Include statistics at the end showing how your choices compared with other players.",
    "Add ambient environmental sounds that respond to narrative tension level.",
    "Consider a photo mode for capturing and sharing favorite AI-generated scene compositions.",
    "Implement an undo option for the most recent choice to reduce frustration.",
    "Add more transitional animations between scenes to improve narrative flow.",
    "Consider episodic content updates that expand the story world over time.",
]

ACCESSIBILITY_DETAILS = [
    "colorblind mode",
    "larger text options",
    "subtitles for all audio",
    "screen reader compatibility",
    "high contrast mode",
    "keyboard-only navigation",
    "reduced motion option",
    "adjustable text speed",
    "colorblind mode and larger text",
    "subtitles and audio descriptions",
    "customizable color schemes",
    "one-handed control support",
    "text-to-speech for dialogue",
    "dyslexia-friendly font option",
    "magnification support",
]

# ---------------------------------------------------------------------------
# 1. Requirements Survey (120 responses)
# ---------------------------------------------------------------------------

def generate_requirements_survey():
    n = 120
    rows = []

    ages = np.clip(np.round(np.random.normal(25, 7, n)).astype(int), 18, 65)
    genders = weighted_choice(
        ["Male", "Female", "Non-binary", "Prefer not to say"],
        [0.52, 0.35, 0.08, 0.05],
        size=n,
    )
    educations = weighted_choice(
        ["High School", "Bachelors", "Masters", "PhD"],
        [0.25, 0.45, 0.22, 0.08],
        size=n,
    )
    gaming_exp = np.clip(np.round(np.random.exponential(7, n)).astype(int), 0, 30)
    hours_weekly = np.clip(np.round(np.random.gamma(3, 4, n)).astype(int), 0, 40)

    genres = weighted_choice(
        ["RPG", "Adventure", "Puzzle", "Strategy", "Action", "Simulation"],
        [0.30, 0.25, 0.12, 0.10, 0.15, 0.08],
        size=n,
    )
    art_styles = weighted_choice(
        ["Pixel Art", "Realistic 3D", "Anime", "Watercolor", "Low Poly"],
        [0.22, 0.18, 0.25, 0.15, 0.20],
        size=n,
    )

    narrative_imp = likert(1, 7, 5.5, 1.2, n)
    character_imp = likert(1, 7, 5.0, 1.3, n)
    world_imp = likert(1, 7, 5.2, 1.2, n)
    music_imp = likert(1, 7, 4.8, 1.4, n)
    gameplay_story = likert(1, 7, 4.0, 1.5, n)

    # AI comfort correlates with gaming experience
    base_ai_comfort = 4.2 + 0.06 * gaming_exp
    ai_comfort = np.clip(
        np.round(np.random.normal(base_ai_comfort, 1.1)).astype(int), 1, 7
    )
    ai_art = np.clip(
        np.round(np.random.normal(base_ai_comfort - 0.3, 1.2)).astype(int), 1, 7
    )
    ai_story = np.clip(
        np.round(np.random.normal(base_ai_comfort + 0.1, 1.1)).astype(int), 1, 7
    )

    game_lengths = weighted_choice(
        [15, 30, 45, 60, 90],
        [0.08, 0.25, 0.30, 0.25, 0.12],
        size=n,
    )
    multiplayer = likert(1, 7, 3.5, 1.8, n)

    accessibility_yn = weighted_choice(["Yes", "No"], [0.15, 0.85], size=n)

    # Prepare open-ended feedback pool
    all_feedback = OPEN_FEEDBACK_POSITIVE + OPEN_FEEDBACK_SKEPTICAL + OPEN_FEEDBACK_MIXED

    for i in range(n):
        pid = f"P{i+1:03d}"
        acc_det = ""
        if accessibility_yn[i] == "Yes":
            acc_det = random.choice(ACCESSIBILITY_DETAILS)

        fb_idx = random.randint(0, len(all_feedback) - 1)
        open_fb = all_feedback[fb_idx]

        rows.append({
            "participant_id": pid,
            "age": int(ages[i]),
            "gender": genders[i],
            "education": educations[i],
            "gaming_experience_years": int(gaming_exp[i]),
            "hours_gaming_weekly": int(hours_weekly[i]),
            "preferred_genre": genres[i],
            "preferred_art_style": art_styles[i],
            "narrative_importance": int(narrative_imp[i]),
            "character_depth_importance": int(character_imp[i]),
            "world_building_importance": int(world_imp[i]),
            "music_importance": int(music_imp[i]),
            "gameplay_over_story": int(gameplay_story[i]),
            "ai_generated_content_comfort": int(ai_comfort[i]),
            "ai_art_acceptance": int(ai_art[i]),
            "ai_story_acceptance": int(ai_story[i]),
            "preferred_game_length_minutes": int(game_lengths[i]),
            "multiplayer_interest": int(multiplayer[i]),
            "accessibility_needs": accessibility_yn[i],
            "accessibility_details": acc_det,
            "open_feedback": open_fb,
        })

    with open(SURVEY_PATH, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(f"[OK] Requirements survey: {len(rows)} rows -> {SURVEY_PATH}")
    return rows


# ---------------------------------------------------------------------------
# 2. Post-test Survey (40 responses)
# ---------------------------------------------------------------------------

def generate_posttest_survey(req_rows):
    n = 40
    rows = []

    for i in range(n):
        pid = f"P{i+1:03d}"
        age = req_rows[i]["age"]
        gender = req_rows[i]["gender"]

        # --- SUS (1-5 Likert) ---
        # Target SUS ~72.  SUS formula: sum( (odd_q - 1) + (5 - even_q) ) * 2.5
        # For score 72 => raw sum ~ 28.8 out of 40
        # Odd questions (positive): mean ~4.0, Even questions (negative): mean ~2.2
        sus = {}
        for q in range(1, 11):
            if q % 2 == 1:  # positive
                sus[f"sus_q{q}"] = int(np.clip(np.round(np.random.normal(4.0, 0.8)), 1, 5))
            else:  # negative
                sus[f"sus_q{q}"] = int(np.clip(np.round(np.random.normal(2.2, 0.9)), 1, 5))

        # --- UES subscales (1-5 Likert) ---
        # Correlation: higher narrative_importance in req survey -> higher engagement
        narr_boost = (req_rows[i]["narrative_importance"] - 4) * 0.12

        engagement = {}
        for q in range(1, 6):
            engagement[f"engagement_fa{q}"] = int(np.clip(
                np.round(np.random.normal(3.6 + narr_boost, 0.8)), 1, 5))
        for q in range(1, 4):
            engagement[f"engagement_pu{q}"] = int(np.clip(
                np.round(np.random.normal(3.8, 0.7)), 1, 5))
        for q in range(1, 5):
            engagement[f"engagement_ae{q}"] = int(np.clip(
                np.round(np.random.normal(3.7 + narr_boost, 0.8)), 1, 5))
        for q in range(1, 4):
            engagement[f"engagement_rw{q}"] = int(np.clip(
                np.round(np.random.normal(3.5, 0.9)), 1, 5))

        # --- Narrative quality (1-7, generally positive 4-6) ---
        narrative_q = {}
        for q in range(1, 6):
            narrative_q[f"narrative_quality_q{q}"] = int(np.clip(
                np.round(np.random.normal(5.0, 0.9)), 1, 7))

        # --- AI perception (1-7, mixed) ---
        ai_boost = (req_rows[i]["ai_generated_content_comfort"] - 4) * 0.2
        ai_perc = {}
        for q in range(1, 6):
            ai_perc[f"ai_perception_q{q}"] = int(np.clip(
                np.round(np.random.normal(4.3 + ai_boost, 1.3)), 1, 7))

        # --- Immersion (1-7) ---
        immersion = {}
        for q in range(1, 4):
            immersion[f"immersion_q{q}"] = int(np.clip(
                np.round(np.random.normal(5.0 + narr_boost, 1.1)), 1, 7))

        # --- Open-ended ---
        pos_text = POSITIVE_FEEDBACK_POSTTEST[i % len(POSITIVE_FEEDBACK_POSTTEST)]
        neg_text = NEGATIVE_FEEDBACK_POSTTEST[i % len(NEGATIVE_FEEDBACK_POSTTEST)]
        sug_text = SUGGESTIONS_POSTTEST[i % len(SUGGESTIONS_POSTTEST)]

        row = {"participant_id": pid, "age": age, "gender": gender}
        row.update(sus)
        row.update(engagement)
        row.update(narrative_q)
        row.update(ai_perc)
        row.update(immersion)
        row["open_positive"] = pos_text
        row["open_negative"] = neg_text
        row["open_suggestions"] = sug_text
        rows.append(row)

    with open(POSTTEST_PATH, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(f"[OK] Post-test survey: {len(rows)} rows -> {POSTTEST_PATH}")
    return rows


# ---------------------------------------------------------------------------
# 3. Interaction Logs JSON (40 participants)
# ---------------------------------------------------------------------------

PAGES = ["intro", "character_creation", "chapter_1", "chapter_2", "chapter_3", "ending"]
EVENT_TYPES = [
    "page_view", "button_click", "choice_made",
    "dialog_interaction", "settings_change", "help_accessed",
]
CHOICE_TEXTS = {
    "chapter_1": [
        ("c1_a", "Trust the mysterious stranger and follow them into the forest"),
        ("c1_b", "Decline the offer and search for another path through the ruins"),
        ("c1_c", "Ask the stranger about their motives before deciding"),
    ],
    "chapter_2": [
        ("c2_a", "Confront the guardian directly with your current abilities"),
        ("c2_b", "Seek the hidden artifact to gain an advantage first"),
        ("c2_c", "Attempt to negotiate a peaceful passage with the guardian"),
    ],
    "chapter_3": [
        ("c3_a", "Sacrifice the artifact to save your companion"),
        ("c3_b", "Keep the artifact and face the final challenge alone"),
        ("c3_c", "Find an alternative solution using knowledge from earlier chapters"),
    ],
}
ERROR_TYPES = [
    "image_load_failure", "audio_playback_error", "text_overflow",
    "save_error", "animation_stutter",
]

DETAIL_TEMPLATES = {
    "page_view": [
        "Navigated to {page} page",
        "Loaded {page} content",
        "Entered {page} section",
    ],
    "button_click": [
        "Clicked continue button on {page}",
        "Clicked inventory button on {page}",
        "Clicked map toggle on {page}",
        "Clicked back button on {page}",
    ],
    "choice_made": [
        "Selected narrative choice on {page}",
    ],
    "dialog_interaction": [
        "Opened dialog with NPC on {page}",
        "Advanced dialog on {page}",
        "Explored dialog option on {page}",
    ],
    "settings_change": [
        "Adjusted text speed on {page}",
        "Changed music volume on {page}",
        "Toggled subtitles on {page}",
    ],
    "help_accessed": [
        "Opened help overlay on {page}",
        "Viewed controls reference on {page}",
    ],
}


def generate_interaction_logs():
    n = 40
    base_time = datetime(2026, 1, 15, 9, 0, 0)
    all_logs = []

    for i in range(n):
        pid = f"P{i+1:03d}"
        session_offset = timedelta(hours=random.randint(0, 72), minutes=random.randint(0, 59))
        session_start = base_time + session_offset
        duration_minutes = random.randint(15, 60)
        session_end = session_start + timedelta(minutes=duration_minutes)
        duration_seconds = duration_minutes * 60

        num_events = random.randint(15, 50)
        events = []
        current_time = session_start + timedelta(seconds=random.randint(1, 10))
        page_idx = 0

        for e in range(num_events):
            # Progress through pages
            if e > 0 and random.random() < 0.15 and page_idx < len(PAGES) - 1:
                page_idx += 1
            page = PAGES[min(page_idx, len(PAGES) - 1)]

            # Weighted event type selection
            if page_idx == 0 and e == 0:
                etype = "page_view"
            else:
                etype_weights = [0.15, 0.25, 0.10, 0.30, 0.08, 0.12]
                etype = random.choices(EVENT_TYPES, weights=etype_weights, k=1)[0]

            detail = random.choice(DETAIL_TEMPLATES.get(etype, ["Interaction on {page}"])).format(page=page)
            time_on_page = random.randint(3, 90)

            events.append({
                "timestamp": current_time.isoformat(),
                "event_type": etype,
                "page": page,
                "details": detail,
                "time_on_page_seconds": time_on_page,
            })

            current_time += timedelta(seconds=random.randint(5, 60))
            if current_time > session_end:
                current_time = session_end - timedelta(seconds=1)

        # Choices
        choices_made = []
        for ch_name, ch_options in CHOICE_TEXTS.items():
            cid, ctext = random.choice(ch_options)
            choices_made.append({
                "chapter": ch_name,
                "choice_id": cid,
                "choice_text": ctext,
                "time_to_decide_seconds": round(random.uniform(3.0, 45.0), 1),
            })

        # Errors (0-3 per participant)
        num_errors = int(np.random.choice([0, 1, 2, 3], p=[0.45, 0.30, 0.18, 0.07]))
        errors = []
        for _ in range(num_errors):
            err_time = session_start + timedelta(seconds=random.randint(60, max(61, duration_seconds - 10)))
            errors.append({
                "timestamp": err_time.isoformat(),
                "error_type": random.choice(ERROR_TYPES),
                "page": random.choice(PAGES),
            })

        total_clicks = sum(1 for ev in events if ev["event_type"] == "button_click")
        total_pages = len(set(ev["page"] for ev in events))

        all_logs.append({
            "participant_id": pid,
            "session_start": session_start.isoformat(),
            "session_end": session_end.isoformat(),
            "session_duration_seconds": duration_seconds,
            "total_clicks": total_clicks,
            "total_pages_visited": total_pages,
            "events": events,
            "choices_made": choices_made,
            "errors_encountered": errors,
        })

    with open(LOGS_PATH, "w") as f:
        json.dump(all_logs, f, indent=2)

    print(f"[OK] Interaction logs: {len(all_logs)} participants -> {LOGS_PATH}")
    return all_logs


# ---------------------------------------------------------------------------
# 4. Coded Qualitative Data
# ---------------------------------------------------------------------------

CODE_MAP = {
    "positive": [
        ("immersive_narrative", "Content Quality"),
        ("visual_quality", "Content Quality"),
        ("creative_choices", "Engagement"),
        ("music_atmosphere", "Content Quality"),
        ("character_development", "Content Quality"),
        ("replayability", "Engagement"),
    ],
    "negative": [
        ("ai_inconsistency", "AI Perception"),
        ("pacing_issues", "User Experience"),
        ("technical_glitch", "Technical Performance"),
        ("ui_navigation", "User Experience"),
        ("visual_quality", "Content Quality"),
    ],
    "suggestion": [
        ("replayability", "Engagement"),
        ("ui_navigation", "User Experience"),
        ("creative_choices", "Engagement"),
        ("character_development", "Content Quality"),
        ("technical_glitch", "Technical Performance"),
    ],
}


def generate_coded_qualitative(posttest_rows):
    rows = []
    coders = ["LLM_coder_1", "LLM_coder_2"]

    for pt in posttest_rows:
        pid = pt["participant_id"]

        for rtype, text_key in [
            ("positive", "open_positive"),
            ("negative", "open_negative"),
            ("suggestion", "open_suggestions"),
        ]:
            text = pt[text_key]
            code, theme = random.choice(CODE_MAP[rtype])

            # Primary coder
            primary_coder = random.choice(coders)
            rows.append({
                "participant_id": pid,
                "response_type": rtype,
                "original_text": text,
                "code": code,
                "theme": theme,
                "coder": primary_coder,
            })

            # Second coder with ~85% agreement
            secondary_coder = coders[0] if primary_coder == coders[1] else coders[1]
            if random.random() < 0.85:
                # Agreement
                rows.append({
                    "participant_id": pid,
                    "response_type": rtype,
                    "original_text": text,
                    "code": code,
                    "theme": theme,
                    "coder": secondary_coder,
                })
            else:
                # Disagreement - assign a different code from the same response type
                alt_codes = [c for c in CODE_MAP[rtype] if c[0] != code]
                alt_code, alt_theme = random.choice(alt_codes) if alt_codes else (code, theme)
                rows.append({
                    "participant_id": pid,
                    "response_type": rtype,
                    "original_text": text,
                    "code": alt_code,
                    "theme": alt_theme,
                    "coder": secondary_coder,
                })

    with open(CODED_PATH, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "participant_id", "response_type", "original_text",
            "code", "theme", "coder",
        ])
        writer.writeheader()
        writer.writerows(rows)

    print(f"[OK] Coded qualitative data: {len(rows)} rows -> {CODED_PATH}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("=" * 70)
    print("Generating Project 1 (Gemini Quest) dummy data ...")
    print("=" * 70)

    req_rows = generate_requirements_survey()
    posttest_rows = generate_posttest_survey(req_rows)
    generate_interaction_logs()
    generate_coded_qualitative(posttest_rows)

    print("=" * 70)
    print("All data generated successfully.")
    print("=" * 70)


if __name__ == "__main__":
    main()
