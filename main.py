"""
VaakKalp - Main Application Entry Point
FastAPI app with persistent session memory across restarts.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uuid
from agents.orchestrator import run_vaakkalp
from session_store import get_session_context, append_message

app = FastAPI(title="VaakKalp", description="Preserving Endangered Oral Heritage")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None
    user_id: str = "default"


class ChatResponse(BaseModel):
    response: str
    session_id: str


@app.get("/health")
def health():
    return {"status": "ok", "service": "vaakkalp"}


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    session_id = req.session_id or str(uuid.uuid4())

    # Inject prior conversation context for memory across restarts
    prior_context = get_session_context(session_id)
    message_with_context = (
        f"{prior_context}{req.message}" if prior_context else req.message
    )

    try:
        response = await run_vaakkalp(
            message_with_context, session_id, req.user_id
        )

        # Persist both turns to disk
        append_message(session_id, req.user_id, "user", req.message)
        append_message(session_id, req.user_id, "agent", response)

        return ChatResponse(response=response, session_id=session_id)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent error: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
