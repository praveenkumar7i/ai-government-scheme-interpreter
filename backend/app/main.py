from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from app.api.middleware.error_handler import global_exception_handler, validation_exception_handler
from app.api.v1.routes_auth import router as auth_router
from app.api.v1.routes_chat import router as chat_router
from app.api.v1.routes_documents import router as documents_router
from app.api.v1.routes_query import router as query_router
from app.core.config import settings
from app.db.session import Base, engine
from app.models import ChatMessage, ChatSession, DocumentChunk, SchemeDocument, User

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

app.include_router(auth_router, prefix=settings.api_prefix)
app.include_router(documents_router, prefix=settings.api_prefix)
app.include_router(query_router, prefix=settings.api_prefix)
app.include_router(chat_router, prefix=settings.api_prefix)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
