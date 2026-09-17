"""
Intent Detection Pipeline (IDP) & Intent Drift Handler (IDH) for AdGeno.

Patent Innovation:
5-Stage Hybrid Intent Classifier:
  Stage 1: Multi-category weighted keyword scoring
  Stage 2: Groq LLM semantic intent classification
  Stage 3: Hybrid confidence calculation: (keyword_score * 0.4) + (llm_score * 0.6)
  Stage 4: Intent Drift Handler (IDH) — detects shift from previous session intent
  Stage 5: Ephemeral Memory trigger flag output
"""

import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Initialize Groq client safely
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

CATEGORIES = [
    "skincare", "travel", "food", "technology", "fashion",
    "health", "fitness", "finance", "education", "entertainment",
    "home", "general"
]

CATEGORY_KEYWORDS = {
    "skincare": [
        "skin", "skincare", "acne", "pimple", "serum", "moisturizer", "cleanser",
        "niacinamide", "salicylic", "ceramide", "glow", "face", "wrinkle", "dark spot",
        "sunscreen", "spf", "dry skin", "oily skin", "pigmentation", "pore", "dermatologist",
        "minimalist", "mamaearth", "cerave", "dot & key", "ordinary", "plum"
    ],
    "travel": [
        "travel", "trip", "flight", "hotel", "vacation", "tour", "resort", "booking",
        "airline", "train", "destination", "homestay", "beach", "mountain", "staycation",
        "makemytrip", "airbnb", "ixigo", "irctc"
    ],
    "food": [
        "food", "eat", "hungry", "dinner", "lunch", "breakfast", "swiggy", "zomato",
        "restaurant", "pizza", "burger", "biryani", "cafe", "snack", "recipe", "delivery"
    ],
    "technology": [
        "laptop", "phone", "smartphone", "gadget", "headphones", "tech", "computer",
        "software", "hardware", "amazon", "croma", "electronics", "ios", "android", "macbook"
    ],
    "fashion": [
        "fashion", "clothes", "dress", "outfit", "wear", "shoes", "sneakers", "myntra",
        "nykaa", "shirt", "jeans", "apparel", "designer", "brand"
    ],
    "health": [
        "health", "doctor", "medicine", "fever", "sick", "hospital", "clinic", "practo",
        "1mg", "symptoms", "checkup", "pharma", "lab test", "vitamin"
    ],
    "fitness": [
        "gym", "workout", "fitness", "cultfit", "exercise", "running", "yoga", "protein",
        "muscle", "weight loss", "decathlon", "cardio", "dumbbells"
    ],
    "finance": [
        "invest", "stock", "trading", "money", "bank", "credit card", "zerodha", "groww",
        "mutual fund", "sip", "crypto", "finance", "savings", "shares"
    ],
    "education": [
        "learn", "course", "coding", "python", "study", "udemy", "coursera", "degree",
        "college", "university", "tutorial", "certification", "student"
    ],
    "entertainment": [
        "movie", "film", "series", "hotstar", "netflix", "spotify", "music", "song",
        "cricket", "stream", "show", "watch", "cinema"
    ],
    "home": [
        "home", "furniture", "decor", "ikea", "sofa", "desk", "bedroom", "kitchen",
        "curtain", "interior", "lighting"
    ]
}


def _stage1_keyword_score(message: str) -> dict:
    """Stage 1: Multi-category weighted keyword scoring."""
    message_lower = message.lower()
    scores = {cat: 0.0 for cat in CATEGORIES}

    for cat, kw_list in CATEGORY_KEYWORDS.items():
        for kw in kw_list:
            if kw in message_lower:
                # Exact word match bonus vs substring
                words = message_lower.split()
                if kw in words:
                    scores[cat] += 2.0
                else:
                    scores[cat] += 1.0

    total = sum(scores.values())
    if total == 0:
        return {"category": "general", "score": 0.0}

    best_cat = max(scores, key=scores.get)
    normalized_score = min(scores[best_cat] / 3.0, 1.0)  # Cap at 1.0
    return {"category": best_cat, "score": normalized_score}


def _stage2_llm_intent(message: str) -> dict:
    """Stage 2: Groq LLM semantic classification."""
    if not client:
        return {"category": "general", "score": 0.5}

    prompt = f"""Analyze the user message and identify the primary topic intent.
Choose EXACTLY ONE category from this list:
[skincare, travel, food, technology, fashion, health, fitness, finance, education, entertainment, home, general]

User message: "{message}"

Return format: CATEGORY (e.g. skincare)
Return ONLY the category name in lowercase.
"""
    MODELS = ["qwen/qwen3.8-27b", "groq/compound-mini", "openai/gpt-oss-120b", "openai/gpt-oss-20b"]
    for model_name in MODELS:
        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=15,
                temperature=0.1
            )
            llm_cat = response.choices[0].message.content.strip().lower()
            for cat in CATEGORIES:
                if cat in llm_cat:
                    return {"category": cat, "score": 0.9}
            break  # Model responded but no category matched
        except Exception as e:
            print(f"[IDP Stage 2 Warning] Model {model_name} failed: {e}")
            continue

    return {"category": "general", "score": 0.3}


def detect_intent_pipeline(message: str, previous_intent: str = None) -> dict:
    """
    Patent-Grade 5-Stage Intent Detection Pipeline (IDP)
    with Intent Drift Handler (IDH).
    """
    # Stage 1: Keyword Scoring
    kw_result = _stage1_keyword_score(message)

    # Stage 2: Semantic LLM Classification
    llm_result = _stage2_llm_intent(message)

    # Stage 3: Hybrid Confidence Calculation
    if kw_result["category"] == llm_result["category"]:
        final_intent = kw_result["category"]
        confidence = round(0.4 * kw_result["score"] + 0.6 * llm_result["score"], 2)
    elif kw_result["score"] >= 0.6:
        # High keyword score overrides uncertain LLM
        final_intent = kw_result["category"]
        confidence = round(kw_result["score"], 2)
    elif llm_result["category"] != "general":
        final_intent = llm_result["category"]
        confidence = round(llm_result["score"], 2)
    else:
        final_intent = "general"
        confidence = 0.5

    # Stage 4: Intent Drift Handler (IDH) — Intent Shift Detection
    is_intent_shifted = False
    if previous_intent and previous_intent != "general":
        if final_intent != previous_intent and final_intent != "general":
            is_intent_shifted = True
            print(f"[IDH Alert] Intent shifted from '{previous_intent}' to '{final_intent}'. Ephemeral context cleared.")

    # Stage 5: Structured Pipeline Output
    return {
        "intent": final_intent,
        "confidence": confidence,
        "is_intent_shifted": is_intent_shifted,
        "previous_intent": previous_intent
    }
