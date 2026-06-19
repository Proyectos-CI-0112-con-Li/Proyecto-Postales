import json
from datetime import datetime
from pathlib import Path
from uuid import uuid4


POSTS_PATH = Path(__file__).resolve().parent.parent / "data" / "posts.json"


def create_post(form_data, catalog):
    owned_codes = set(form_data.getlist("owned_codes"))
    repeated_cards = []
    missing_cards = []

    for card in catalog:
        code = card["code"]
        quantity = _parse_quantity(form_data.get(f"duplicate_quantity_{code}", "0"))

        if quantity > 0:
            repeated_cards.append({**card, "quantity": quantity})
            owned_codes.add(code)

        if code not in owned_codes:
            missing_cards.append(card)

    post = {
        "id": str(uuid4()),
        "person_name": form_data.get("person_name", "").strip() or "Sin nombre",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "repeated_cards": repeated_cards,
        "missing_cards": missing_cards,
    }

    posts = get_posts()
    posts.insert(0, post)
    _save_posts(posts)
    return post


def get_posts():
    if not POSTS_PATH.exists():
        return []

    try:
        with POSTS_PATH.open("r", encoding="utf-8") as posts_file:
            posts = json.load(posts_file)
    except (json.JSONDecodeError, OSError):
        return []

    if not isinstance(posts, list):
        return []

    return posts


def _parse_quantity(value):
    try:
        return max(0, int(value))
    except (TypeError, ValueError):
        return 0


def _save_posts(posts):
    POSTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with POSTS_PATH.open("w", encoding="utf-8") as posts_file:
        json.dump(posts, posts_file, ensure_ascii=False, indent=2)
