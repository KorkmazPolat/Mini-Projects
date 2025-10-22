from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .extractor import get_duration_info, ExtractionError


app = FastAPI(title="YouTube Duration Service", version="1.0.0")

# Allow all origins for convenience; adjust as needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class URLRequest(BaseModel):
    url: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/duration")
def get_duration(url: str = Query(..., description="YouTube video URL")):
    try:
        info = get_duration_info(url)
        return info
    except ExtractionError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Failed to resolve duration: {e}")


@app.post("/duration")
def post_duration(body: URLRequest):
    try:
        info = get_duration_info(body.url)
        return info
    except ExtractionError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Failed to resolve duration: {e}")

