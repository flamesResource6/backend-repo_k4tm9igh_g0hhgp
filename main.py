import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

from database import db, create_document, get_documents
from schemas import Inquiry

app = FastAPI(title="Blue Flame Catering API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Blue Flame Catering backend running"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set",
        "database_name": "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set",
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️ Connected but Error: {str(e)[:80]}"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:80]}"

    return response

# Inquiries endpoints
@app.post("/inquiries")
def create_inquiry(inquiry: Inquiry):
    try:
        doc_id = create_document("inquiry", inquiry)
        return {"status": "ok", "id": doc_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/inquiries")
def list_inquiries(limit: int = 50):
    try:
        docs = get_documents("inquiry", limit=limit)
        # Convert ObjectId to string and datetime to isoformat
        for d in docs:
            if "_id" in d:
                d["_id"] = str(d["_id"])
            if "created_at" in d:
                d["created_at"] = d["created_at"].isoformat() if hasattr(d["created_at"], 'isoformat') else d["created_at"]
            if "updated_at" in d:
                d["updated_at"] = d["updated_at"].isoformat() if hasattr(d["updated_at"], 'isoformat') else d["updated_at"]
        return {"items": docs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
