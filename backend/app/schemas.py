from pydantic import BaseModel
from typing import Optional, List

class ChatRequest(BaseModel):
    session_id: str
    message: str
    images: Optional[List[str]] = None  # List of base64 strings
    file_context: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    ad: Optional[dict] = None
    intent: Optional[str] = None

class TranscriptionResponse(BaseModel):
    text: str

class AdBase(BaseModel):
    title: str
    description: str
    url: str
    keywords: List[str]
    category: str

class AdCreate(AdBase):
    pass

class AdResponse(AdBase):
    id: int

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    session_id: str
    preferences: Optional[str] = None
    current_intent: Optional[str] = None

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True