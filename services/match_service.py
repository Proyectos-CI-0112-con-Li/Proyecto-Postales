def get_ranked_matches(target_post, all_posts):
    target_missing = {card["code"] for card in target_post["missing_cards"]}
    ranked_matches = []

    for candidate in all_posts:
        if candidate["id"] == target_post["id"]:
            continue

        useful_cards = [
            card for card in candidate["repeated_cards"] if card["code"] in target_missing
        ]
        if not useful_cards:
            continue

        candidate_missing = {card["code"] for card in candidate["missing_cards"]}
        reciprocal_cards = [
            card
            for card in target_post["repeated_cards"]
            if card["code"] in candidate_missing
        ]
        useful_score = sum(card["quantity"] for card in useful_cards)
        reciprocal_score = sum(card["quantity"] for card in reciprocal_cards)

        ranked_matches.append(
            {
                "post": candidate,
                "useful_cards": useful_cards,
                "reciprocal_cards": reciprocal_cards,
                "score": useful_score + reciprocal_score,
            }
        )

    return sorted(ranked_matches, key=lambda item: item["score"], reverse=True)
