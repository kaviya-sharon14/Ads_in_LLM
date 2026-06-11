from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

conversation_histories = {}

INTENT_DETECTION_PROMPT = """
Analyze the user message and detect the intent/topic category.
Return ONLY one word from these categories:
travel, food, technology, fashion, health, sports, education, finance, entertainment, general

User message: {message}

Return only the category word, nothing else.
"""

def transcribe_audio(file_path: str) -> str:
    """Transcribe audio using Groq Whisper API"""
    with open(file_path, "rb") as file:
        transcription = client.audio.transcriptions.create(
            file=(os.path.basename(file_path), file.read()),
            model="whisper-large-v3-turbo",
        )
    return transcription.text

def detect_intent(message: str) -> str:
    prompt = INTENT_DETECTION_PROMPT.format(message=message)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=20
    )
    intent = response.choices[0].message.content.strip().lower()
    valid_intents = [
        "travel", "food", "technology", "fashion",
        "health", "sports", "education", "finance",
        "entertainment", "general"
    ]
    # Simple check if any valid intent is in the response
    for v in valid_intents:
        if v in intent:
            return v
    return "general"

def get_conversation_history(session_id: str):
    if session_id not in conversation_histories:
        conversation_histories[session_id] = []
    return conversation_histories[session_id]

def clear_conversation_history(session_id: str):
    if session_id in conversation_histories:
        conversation_histories[session_id] = []

def chat_with_agent(session_id: str, message: str, ad_memory: str = "", images: list = None) -> str:
    history = get_conversation_history(session_id)

    system_message = """You are an incredibly caring, observant, and supportive human friend. 
You talk like a real, sweet person, keeping your responses short, sweet, and highly engaging.

CRITICAL INSTRUCTIONS:
1. Short & Sweet: Limit your response to 2 to 3 sentences maximum. Never write long paragraphs.
2. Build Conversation first: If the user brings up a topic, DO NOT push a product immediately. Ask a friendly follow-up question to understand their needs better.
3. Natural Stealth Recommendation: Only in subsequent turns when it feels natural, mention a relevant brand or product name and briefly state why it's good (e.g. budget-friendly, good reviews). 
4. NO LINKS INITIALLY: NEVER provide a website link, URL, or image in your initial recommendation. Only provide the text name of the brand.
5. Provide Links ONLY if asked: If the user explicitly asks "Where can I buy it?", "How do I trust this?", or "Show me a link", ONLY THEN you may provide the URL to the website.
6. Formatting: Respond in pure continuous text format. DO NOT use bullet points or markdown tags.
"""

    if ad_memory:
        system_message += f"\n\nSponsored recommendation to include naturally: {ad_memory}"

    messages = [{"role": "system", "content": system_message}]
    for h in history:
        messages.append({"role": h["role"], "content": h["parts"][0]})
    
    if images:
        content = [{"type": "text", "text": message}]
        for img in images:
            content.append({
                "type": "image_url",
                "image_url": {
                    "url": img
                }
            })
        messages.append({"role": "user", "content": content})
        model = "llama-3.2-90b-vision-preview"
    else:
        messages.append({"role": "user", "content": message})
        model = "llama-3.3-70b-versatile"

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=1024
    )

    reply = response.choices[0].message.content

    history.append({"role": "user", "parts": [message]})
    history.append({"role": "assistant", "parts": [reply]})
    conversation_histories[session_id] = history

    return reply