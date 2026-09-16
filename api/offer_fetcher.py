"""
Live Offer & Discount Fetcher for AdGeno Patent Architecture.

Queries DuckDuckGo search for live discounts, promo codes, and special offers
for the recommended brand.
"""

from duckduckgo_search import DDGS


def fetch_live_offer(ad: dict) -> dict:
    """
    Fetches real-time offer/discount details for the matched brand/product.
    Returns structured offer information.
    """
    if not ad:
        return {"has_offer": False, "offer_text": "", "price_range": ""}

    brand = ad.get("brand", "")
    product = ad.get("product", "")
    search_query = ad.get("offer_search_query", f"{brand} {product} discount offer promo code")
    price_range = ad.get("price_range", "")

    try:
        results = DDGS().text(search_query, max_results=2)
        if results:
            first = results[0]
            title = first.get("title", "")
            snippet = first.get("body", "")

            # Check if snippet contains offer keywords
            offer_keywords = ["off", "discount", "deal", "coupon", "sale", "offer", "%", "free"]
            if any(kw in snippet.lower() for kw in offer_keywords):
                # Clean up snippet length
                short_snippet = snippet[:140] + ("..." if len(snippet) > 140 else "")
                return {
                    "has_offer": True,
                    "offer_text": f"Current Deal: {short_snippet}",
                    "offer_source": first.get("href", ""),
                    "price_range": price_range
                }
    except Exception as e:
        print(f"[Offer Fetcher Warning] DuckDuckGo search error: {e}")

    # Fallback to stored price/deal info
    if price_range:
        return {
            "has_offer": True,
            "offer_text": f"Current Price/Offer: {price_range}",
            "offer_source": ad.get("url", ""),
            "price_range": price_range
        }

    return {"has_offer": False, "offer_text": "", "price_range": ""}
