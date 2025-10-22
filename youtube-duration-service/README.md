YouTube Duration Service

Small FastAPI service that accepts a YouTube URL and returns the video duration.

Features
- Extracts duration using `yt-dlp` only (no API key)
- Simple REST endpoints for GET and POST

Quick Start
1) Create and activate a virtualenv (recommended)

   - macOS/Linux:
     python3 -m venv .venv
     source .venv/bin/activate

   - Windows (PowerShell):
     py -3 -m venv .venv
     .venv\\Scripts\\Activate.ps1

2) Install dependencies
   pip install -r requirements.txt

3) Run the service
   uvicorn app.main:app --reload

4) Call the API
   - GET example:
     curl "http://127.0.0.1:8000/duration?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ"

   - POST example:
     curl -X POST http://127.0.0.1:8000/duration \
       -H "Content-Type: application/json" \
       -d '{"url":"https://youtu.be/dQw4w9WgXcQ"}'

Response (example)
{
  "id": "dQw4w9WgXcQ",
  "title": "Rick Astley - Never Gonna Give You Up (Official Music Video)",
  "duration_seconds": 213,
  "duration_human": "00:03:33",
  "source": "yt_dlp"
}

Configuration
- No API key required. The service relies on `yt-dlp` only.

Endpoints
- GET `/duration?url=...`
- POST `/duration` with JSON body: `{ "url": "..." }`

Notes
- `yt-dlp` is required and does not need an API key.
- The service makes outbound network requests at runtime to resolve video metadata.
