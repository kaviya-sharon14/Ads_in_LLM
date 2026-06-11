from fastapi import FastAPI, Depends, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import shutil
import tempfile
import os
from .database import engine, Base, get_db
from .models import Ad, User
from .schemas import ChatRequest, ChatResponse, TranscriptionResponse
from .agent import detect_intent, chat_with_agent, transcribe_audio
from .ad_engine import (
    get_ads_by_intent,
    get_or_create_user,
    update_user_intent,
    inject_ad_to_memory,
    select_best_ad,
    search_web_for_recommendation
)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Ads in LLM API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Ads in LLM API is running!"}

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    session_id = request.session_id
    message = request.message
    images = request.images
    file_context = request.file_context

    user = get_or_create_user(db, session_id)

    # If file context exists, prepend it to the message for the agent
    full_message = f"{file_context}\n\n{message}" if file_context else message

    intent = detect_intent(full_message)

    previous_intent = user.current_intent
    if intent != previous_intent:
        update_user_intent(db, session_id, intent)

    ads = get_ads_by_intent(db, intent)
    best_ad = select_best_ad(ads)
    
    # Live Web Search fallback
    if not best_ad or intent == "general":
        live_ad = search_web_for_recommendation(intent, full_message)
        if live_ad:
            best_ad = live_ad

    ad_memory = inject_ad_to_memory(best_ad)

    response_text = chat_with_agent(session_id, full_message, ad_memory, images)

    ad_data = None
    if best_ad:
        if isinstance(best_ad, dict):
            ad_data = best_ad
            ad_data["id"] = 0
        else:
            ad_data = {
                "id": best_ad.id,
                "title": best_ad.title,
                "description": best_ad.description,
                "url": best_ad.url,
                "category": best_ad.category
            }

    return ChatResponse(
        response=response_text,
        ad=ad_data,
        intent=intent
    )

@app.post("/transcribe", response_model=TranscriptionResponse)
async def transcribe(file: UploadFile = File(...)):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = tmp.name
        
        text = transcribe_audio(tmp_path)
        os.remove(tmp_path)
        return TranscriptionResponse(text=text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ads/seed")
def seed_ads(db: Session = Depends(get_db)):
    sample_ads = [
        Ad(title="Book Cheap Flights",
           description="Find the best deals on flights worldwide!",
           url="https://www.makemytrip.com",
           keywords=["travel", "flight", "trip", "vacation"],
           category="travel"),
        Ad(title="Order Food Online",
           description="Get your favorite food delivered in 30 minutes!",
           url="https://www.swiggy.com",
           keywords=["food", "delivery", "restaurant", "eat"],
           category="food"),
        Ad(title="Latest Smartphones",
           description="Shop the newest phones at the best prices!",
           url="https://www.amazon.in",
           keywords=["technology", "phone", "gadget", "tech"],
           category="technology"),
        Ad(title="Online Health Consultation",
           description="Consult top doctors from home instantly!",
           url="https://www.practo.com",
           keywords=["health", "doctor", "medical", "fitness"],
           category="health"),
        Ad(title="Learn Programming Online",
           description="Master coding with expert-led courses!",
           url="https://www.udemy.com",
           keywords=["education", "coding", "course", "learn"],
           category="education"),
        Ad(title="Stock Market Investing",
           description="Start investing in stocks with zero commission!",
           url="https://zerodha.com",
           keywords=["finance", "stock", "invest", "money"],
           category="finance"),
    ]

    for ad in sample_ads:
        existing = db.query(Ad).filter(Ad.title == ad.title).first()
        if not existing:
            db.add(ad)

    db.commit()
    return {"message": "Sample ads seeded successfully!"}