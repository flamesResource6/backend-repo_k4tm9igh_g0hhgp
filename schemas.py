from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class Inquiry(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    date: str = Field(..., description="Event date in ISO format (YYYY-MM-DD)")
    guests: int = Field(..., ge=1, le=5000)
    details: Optional[str] = Field(None, max_length=2000)
