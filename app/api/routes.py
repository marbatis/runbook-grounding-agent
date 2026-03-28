from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas.models import AskRequest, QAResponse
from app.services.qa_service import QAService

router = APIRouter(prefix="/api", tags=["api"])


def get_qa_service(db: Session = Depends(get_db)) -> QAService:
    return QAService(db)


@router.post("/qa/ask", response_model=QAResponse, status_code=status.HTTP_201_CREATED)
def ask_question(
    payload: AskRequest,
    service: QAService = Depends(get_qa_service),
) -> QAResponse:
    return service.ask(question=payload.question, service_filter=payload.service_filter)


@router.get("/qa/{query_id}", response_model=QAResponse)
def get_result(query_id: str, service: QAService = Depends(get_qa_service)) -> QAResponse:
    result = service.get(query_id)
    if not result:
        raise HTTPException(status_code=404, detail="Query result not found")
    return result


@router.get("/runbooks")
def list_runbooks(service: QAService = Depends(get_qa_service)) -> dict[str, list[str]]:
    return {"runbooks": service.list_runbooks()}


@router.get("/history")
def list_history(
    limit: int = Query(default=20, ge=1, le=200),
    service: QAService = Depends(get_qa_service),
) -> dict[str, list[dict]]:
    rows = service.history(limit=limit)
    return {"items": [row.model_dump(mode="json") for row in rows]}
