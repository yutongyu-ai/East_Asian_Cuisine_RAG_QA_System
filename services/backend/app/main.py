from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

from .rag.pipeline import RagService

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
rag_instances: Dict[str, RagService] = {}

class ChatRequest(BaseModel):
    session_id: str
    message: str

def get_rag(session_id: str) -> RagService:
    if session_id not in rag_instances:
        rag_instances[session_id] = RagService(session_id=session_id)

    return rag_instances[session_id]

def stream_generator(rag: RagService, question: str):
    full_answer = ""
    try:
        for chunk in rag.chain.stream(question):
            if chunk:
                full_answer += chunk
                yield f"data: {chunk}\n\n" #

        # 👉 最后统一写入 memory（必须等完整回答）
        rag.memory.history.add_user_message(question)
        rag.memory.history.add_ai_message(full_answer)
        yield "data: [DONE]\n\n"

    except Exception as e:
        yield f"data: ERROR: {str(e)}\n\n"


@app.post("/chat")
def chat(req: ChatRequest):
    print("🔥 /chat endpoint hit")
    rag = get_rag(req.session_id)

    return StreamingResponse(
        stream_generator(rag, req.message),
        media_type="text/event-stream"
    )