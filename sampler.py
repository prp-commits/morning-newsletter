"""
sampler.py — Picks ideas for today's newsletter email.

Loads the idea bank, checks the sent log, selects N unsent ideas
for the day's theme, and records what was sent.
"""

import json
import os
import random
from datetime import datetime, date
from typing import List, Optional, Tuple


def load_idea_bank(bank_dir: str) -> List[dict]:
    """Load all ideas from all JSON files in the bank directory."""
    ideas = []
    for fname in sorted(os.listdir(bank_dir)):
        if not fname.endswith(".json"):
            continue
        path = os.path.join(bank_dir, fname)
        with open(path) as f:
            data = json.load(f)
        book_meta = data["book"]
        for idea in data["ideas"]:
            idea["_book_title"] = book_meta["title"].split(":")[0].strip()
            idea["_book_author"] = book_meta["authors"][0]
            ideas.append(idea)
    return ideas


def load_sent_log(log_path: str) -> dict:
    """Load the sent log. Structure: {"sent": ["id1", ...], "favorite_index": 0, "history": [...]}"""
    if os.path.exists(log_path):
        with open(log_path) as f:
            return json.load(f)
    return {"sent": [], "favorite_index": 0, "history": []}


def save_sent_log(log_path: str, log: dict):
    with open(log_path, "w") as f:
        json.dump(log, f, indent=2)


def get_today_theme(config: dict) -> Optional[str]:
    """Return today's theme based on day of week."""
    day_name = datetime.now().strftime("%A").lower()
    return config["schedule"].get(day_name)


def pick_ideas(
    ideas: List[dict],
    theme: str,
    count: int,
    sent_ids: List[str],
) -> List[dict]:
    """Pick `count` unsent ideas for the given theme. Falls back to re-sending if exhausted."""
    pool = [i for i in ideas if theme in i.get("themes", []) and i["id"] not in sent_ids]

    # If pool is exhausted, reset sent history for this theme
    if len(pool) < count:
        pool = [i for i in ideas if theme in i.get("themes", [])]
        # Remove the IDs we're about to re-use from sent_ids (handled by caller)

    random.shuffle(pool)
    return pool[:count]


def pick_favorite(
    ideas: List[dict],
    config: dict,
    sent_log: dict,
) -> List[dict]:
    """Pick 1 idea for Saturday 'favorite' — rotates through themes on a 5-week cycle."""
    cycle = config["favorite_cycle"]
    idx = sent_log.get("favorite_index", 0) % len(cycle)
    theme = cycle[idx]

    # Pick the most recent unsent idea from this theme
    pool = [i for i in ideas if theme in i.get("themes", []) and i["id"] not in sent_log["sent"]]
    if not pool:
        pool = [i for i in ideas if theme in i.get("themes", [])]

    random.shuffle(pool)
    pick = pool[0] if pool else None

    # Advance the cycle
    sent_log["favorite_index"] = idx + 1

    return [pick] if pick else []


def sample_for_today(config: dict) -> Tuple[Optional[str], List[dict], Optional[str]]:
    """
    Main entry point. Returns (theme, list_of_ideas, register).
    Also updates the sent log on disk.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    bank_dir = os.path.join(base_dir, config["idea_bank_dir"])
    log_path = os.path.join(base_dir, config["sent_log"])

    ideas = load_idea_bank(bank_dir)
    sent_log = load_sent_log(log_path)
    theme = get_today_theme(config)

    if theme is None:
        return None, [], None

    if theme == "favorite":
        picks = pick_favorite(ideas, config, sent_log)
        register = "conceptual"
        # Find the actual theme of the picked idea for display
        if picks:
            display_theme = next(
                (t for t in config["favorite_cycle"] if t in picks[0].get("themes", [])),
                "favorite",
            )
        else:
            display_theme = "favorite"
        theme = f"favorite ({display_theme})"
    else:
        count = config["ideas_per_email"]
        picks = pick_ideas(ideas, theme, count, sent_log["sent"])
        register = config["register"].get(theme, "conceptual")

    # Record sent IDs
    for idea in picks:
        if idea["id"] not in sent_log["sent"]:
            sent_log["sent"].append(idea["id"])

    # Record history
    sent_log["history"].append({
        "date": date.today().isoformat(),
        "theme": theme,
        "ids": [i["id"] for i in picks],
    })

    save_sent_log(log_path, sent_log)
    return theme, picks, register


if __name__ == "__main__":
    # Quick test
    base_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(base_dir, "config.json")) as f:
        config = json.load(f)

    theme, picks, register = sample_for_today(config)
    print(f"Theme: {theme} ({register})")
    print(f"Ideas: {len(picks)}")
    for p in picks:
        print(f"  [{p['id']}] {p['headline']}")
        print(f"    — {p['_book_author']}, {p['_book_title']}")