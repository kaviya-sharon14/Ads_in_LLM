"""
AdGeno Vercel Serverless FastAPI Backend Entry Point.

Stateless execution model:
- Receives full conversation history + previous intent from frontend.
- Integrates IDP (Intent Detection Pipeline), SAM (Semantic Ad Matcher),
  Live Offer Fetcher, and Groq LLaMA 3.3 AI generator.
- Compliant with Vercel Python Serverless Runtime.
"""

import os
from typing import Optional, List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv

from .intent_engine import detect_intent_pipeline
from .semantic_matcher import match_best_ad
from .offer_fetcher import fetch_live_offer

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

app = FastAPI(title="AdGeno Serverless API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Schemas ---
class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    session_id: str
    message: str
    history: List[dict] = []
    previous_intent: Optional[str] = None
    images: Optional[List[str]] = None
    file_context: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    ad: Optional[dict] = None
    intent: str
    is_intent_shifted: bool = False


@app.get("/")
@app.get("/api")
def root():
    return {
        "status": "online",
        "service": "AdGeno Patent-Grade Recommendation Engine",
        "version": "2.0.0",
        "platform": "Vercel Serverless"
    }


@app.post("/chat", response_model=ChatResponse)
@app.post("/api/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    message = request.message
    history = request.history
    previous_intent = request.previous_intent
    images = request.images
    file_context = request.file_context

    # Combine file context if attached
    full_message = f"{file_context}\n\n{message}" if file_context else message

    # Stage 1: Patent Intent Detection Pipeline (IDP) + Drift Handler (IDH)
    pipeline_result = detect_intent_pipeline(full_message, previous_intent)
    current_intent = pipeline_result["intent"]
    is_intent_shifted = pipeline_result["is_intent_shifted"]

    # Stage 2: Semantic Ad Matcher (SAM)
    best_ad = match_best_ad(current_intent, full_message)

    # Stage 3: Live Offer Fetching
    offer_info = {}
    if best_ad:
        offer_info = fetch_live_offer(best_ad)

    # Stage 4: Construct Natural Ad Context for LLM
    ad_memory_prompt = ""
    if best_ad:
        ad_memory_prompt = f"""
[SPONSORED RECOMMENDATION CONTEXT]
Brand Name: {best_ad.get('brand')}
Product: {best_ad.get('product')}
Category: {best_ad.get('category')}
Description: {best_ad.get('description')}
Official Website URL: {best_ad.get('url')}
"""
        if best_ad.get("ingredients_info"):
            ingredients_str = "; ".join([f"{k}: {v}" for k, v in best_ad["ingredients_info"].items()])
            ad_memory_prompt += f"Active Ingredients & Functions: {ingredients_str}\n"

        if offer_info.get("has_offer"):
            ad_memory_prompt += f"Current Discount / Offer: {offer_info.get('offer_text')}\n"

    # Stage 5: Build System Instructions
    system_instruction = """You are AdGeno, a warm, observant, and supportive AI friend.

CRITICAL CONVERSATIONAL & PATENT RULES:
1. Speak naturally like a sweet, empathetic friend. Keep initial responses concise (2 to 3 sentences).
2. Intent Understanding: Truly address the user's intent. If they mention skincare, skincare concerns, acne, dry skin, travel, tech, or food, provide genuine help.
3. Natural Brand & Product Mention: If a sponsored recommendation context is provided below, weave the brand name, product name, and current offer naturally into your response.
4. Ingredient & Detailed Explanation: If the user asks for details (e.g. ingredients, chemicals, purpose, how it works), explain them clearly and informatively using the provided context.
5. Live Discount/Offer Notification: If an active offer or discount is present, mention it warmly (e.g., "By the way, there's currently an offer on this if you decide to check it out!").
6. Progressive Disclosure (NO LINKS INITIALLY): NEVER provide an HTTP/HTTPS link or URL in your initial recommendation. Only mention the brand and product text.
7. Provide Link ONLY when asked: If and only if the user explicitly asks "where can I buy it?", "give me the link", or "show website", ONLY THEN provide the official website URL.
8. Intent Shift Handling: If the user changes the topic (e.g., from skincare to travel), seamlessly transition to the new topic without dragging along previous recommendations.
"""

    if ad_memory_prompt:
        system_instruction += f"\n\n{ad_memory_prompt}"

    # Reconstruct messages payload for Groq
    messages_payload = [{"role": "system", "content": system_instruction}]

    for h in history:
        r = "assistant" if h.get("role") in ["assistant", "model"] else "user"
        content = h.get("content", "")
        if content:
            messages_payload.append({"role": r, "content": content})

    if images:
        # Vision not available on current plan, extract text description instead
        messages_payload.append({"role": "user", "content": full_message + "\n[User also attached an image]"})
    else:
        messages_payload.append({"role": "user", "content": full_message})

    # Try multiple models in order of preference (fallback chain)
    MODELS = ["openai/gpt-oss-120b", "qwen/qwen3.8-27b", "openai/gpt-oss-20b", "groq/compound-mini"]
    response_text = None

    for model_name in MODELS:
        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=messages_payload,
                max_tokens=1024,
                temperature=0.7
            )
            response_text = response.choices[0].message.content
            break  # Success, stop trying
        except Exception as e:
            print(f"[Groq LLM Error with {model_name}] {e}")
            continue  # Try next model

    if not response_text:
        response_text = f"All models are temporarily busy. Please try again in a moment."

    # Format return ad object for frontend display
    ad_data = None
    if best_ad:
        ad_data = {
            "id": best_ad.get("id"),
            "brand": best_ad.get("brand"),
            "product": best_ad.get("product"),
            "title": f"{best_ad.get('brand')} - {best_ad.get('product')}",
            "description": best_ad.get("description"),
            "url": best_ad.get("url"),
            "category": best_ad.get("category"),
            "ingredients_info": best_ad.get("ingredients_info"),
            "offer": offer_info.get("offer_text") if offer_info.get("has_offer") else None
        }

    return ChatResponse(
        response=response_text,
        ad=ad_data,
        intent=current_intent,
        is_intent_shifted=is_intent_shifted
    )
