"""
Semantic Ad Matcher (SAM) for AdGeno Patent Architecture.

Patent Innovation:
Pure algorithmic multi-factor relevance scoring without machine learning dependencies:
  relevance_score = (category_match * 0.50)
                  + (keyword_overlap * 0.30)
                  + (subcategory_match * 0.15)
                  + (message_context_density * 0.05)
"""

from .ad_database import get_all_ads


def calculate_ad_relevance(ad: dict, intent: str, message: str) -> float:
    """Calculates multi-factor relevance score for a given ad against user intent and message."""
    message_lower = message.lower()
    msg_words = set(message_lower.split())

    # 1. Category Match (50% weight)
    cat_match = 1.0 if ad.get("category", "").lower() == intent.lower() else 0.0

    # 2. Keyword Overlap (30% weight)
    keywords = ad.get("keywords", [])
    if keywords:
        matched_kw = sum(1 for kw in keywords if kw.lower() in message_lower)
        kw_score = min(matched_kw / max(len(keywords) * 0.3, 1), 1.0)
    else:
        kw_score = 0.0

    # 3. Subcategory Match (15% weight)
    subcat = ad.get("subcategory", "").lower()
    subcat_words = set(subcat.replace("-", " ").split())
    subcat_score = 1.0 if subcat_words & msg_words else 0.0

    # 4. Context Density (5% weight)
    brand_mentioned = 1.0 if ad.get("brand", "").lower() in message_lower else 0.0

    # Weighted Sum Formula
    total_score = (
        (cat_match * 0.50) +
        (kw_score * 0.30) +
        (subcat_score * 0.15) +
        (brand_mentioned * 0.05)
    )

    return round(total_score, 4)


def match_best_ad(intent: str, message: str) -> dict:
    """
    Scores all ads in the database and returns the highest relevance ad.
    Returns None if intent is general and no keywords match.
    """
    ads = get_all_ads()
    scored_ads = []

    for ad in ads:
        score = calculate_ad_relevance(ad, intent, message)
        if score > 0.1:  # Threshold filter
            scored_ads.append((score, ad))

    if not scored_ads:
        return None

    # Sort descending by relevance score
    scored_ads.sort(key=lambda x: x[0], reverse=True)
    best_score, best_ad = scored_ads[0]

    # Attach calculated relevance score to ad metadata
    ad_with_meta = dict(best_ad)
    ad_with_meta["relevance_score"] = best_score
    return ad_with_meta
