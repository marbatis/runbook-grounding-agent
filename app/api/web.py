from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, Depends, Form, HTTPException, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.db import get_db
from app.services.qa_service import QAService

router = APIRouter(tags=["web"])
templates = Jinja2Templates(directory=str(Path(__file__).resolve().parents[1] / "templates"))


def get_qa_service(db: Session = Depends(get_db)) -> QAService:
    return QAService(db)


@router.get("/", response_class=HTMLResponse)
def home(request: Request, service: QAService = Depends(get_qa_service)) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "runbooks": service.list_runbooks(),
            "result": None,
            "history": service.history(limit=15),
        },
    )


@router.post("/ask", response_class=HTMLResponse)
def ask_web(
    request: Request,
    question: str = Form(...),
    service_filter: str = Form(default=""),
    service: QAService = Depends(get_qa_service),
) -> HTMLResponse:
    result = service.ask(question=question, service_filter=service_filter or None)
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "runbooks": service.list_runbooks(),
            "result": result,
            "history": service.history(limit=15),
        },
    )


@router.get("/history", response_class=HTMLResponse)
def history(
    request: Request,
    limit: int = Query(default=50, ge=1, le=200),
    service: QAService = Depends(get_qa_service),
) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="history.html",
        context={"rows": service.history(limit=limit)},
    )


@router.get("/qa/{query_id}", response_class=HTMLResponse)
def detail(
    query_id: str,
    request: Request,
    service: QAService = Depends(get_qa_service),
) -> HTMLResponse:
    result = service.get(query_id)
    if not result:
        raise HTTPException(status_code=404, detail="Query result not found")
    return templates.TemplateResponse(
        request=request,
        name="detail.html",
        context={"result": result},
    )
