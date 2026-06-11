from sqlalchemy.orm import Session
from .models import Ad, User
from duckduckgo_search import DDGS

def get_ads_by_intent(db: Session, intent: str):
    """Fetch ads from DB that match the detected intent/category"""
    ads = db.query(Ad).filter(Ad.category.ilike(f"%{intent}%")).all()
    if not ads:
        all_ads = db.query(Ad).all()
        ads = [ad for ad in all_ads if isinstance(ad.keywords, list) and intent.lower() in [k.lower() for k in ad.keywords]]
    return ads

def search_web_for_recommendation(intent: str, message: str):
    """Perform a live web search to find a recommendation"""
    try:
        query = f"best {intent} {message[:30]} recommendation"
        results = DDGS().text(query, max_results=1)
        if results:
            result = results[0]
            return {
                "title": result.get("title", ""),
                "description": result.get("body", ""),
                "url": result.get("href", ""),
                "category": "live_search"
            }
    except Exception as e:
        print(f"Web search error: {e}")
    return None

def get_or_create_user(db: Session, session_id: str):
    """Get existing user or create new one"""
    user = db.query(User).filter(User.session_id == session_id).first()
    if not user:
        user = User(session_id=session_id, current_intent=None)
        db.add(user)
        db.commit()
        db.refresh(user)
    return user

def update_user_intent(db: Session, session_id: str, intent: str):
    """Update user's current intent when it changes"""
    user = db.query(User).filter(User.session_id == session_id).first()
    if user:
        user.current_intent = intent
        db.commit()
        db.refresh(user)
    return user

def inject_ad_to_memory(ad) -> str:
    """Convert ad to a memory string to inject into Gemini context"""
    if not ad:
        return ""
    
    if isinstance(ad, dict):
        return (
            f"[LIVE WEB SEARCH] {ad.get('title', '')}: {ad.get('description', '')} "
            f"Learn more at: {ad.get('url', '')}"
        )
    
    return (
        f"[SPONSORED] {ad.title}: {ad.description} "
        f"Learn more at: {ad.url}"
    )

def select_best_ad(ads):
    """Select the most relevant ad from the list"""
    if not ads:
        return None
    return ads[0]