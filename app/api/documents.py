"""
HTTP API for knowledge-base document ingestion.

Identity and tenant information always come from AppContext rather than
request parameters.

Current implementation accepts small UTF-8 text files synchronously.
Large documents should use the background ingestion architecture documented
in ARCHITECTURE.md.
"""

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

from app.auth.context import AppContext
from app.auth.dependencies import get_app_context
from app.schemas.document import DocumentUploadResponse
from app.services.documents.ingestion_service import ingest_document

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


@router.post(
    "",
    response_model=DocumentUploadResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_document(
    file: UploadFile = File(...),
    context: AppContext = Depends(get_app_context),
) -> DocumentUploadResponse:
    """Ingest a small text document into the authenticated tenant."""

    if not context.has_permission("documents:create"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions",
        )

    if file.content_type not in {"text/plain"}:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Only UTF-8 text files are currently supported",
        )

    content_bytes = await file.read()

    # Keep synchronous ingestion intentionally bounded.
    # Large files belong in object storage + background processing.
    if len(content_bytes) > 1_000_000:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="File exceeds the synchronous ingestion limit",
        )

    try:
        content = content_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must contain valid UTF-8 text",
        ) from exc

    document_id = await ingest_document(
        tenant_id=context.tenant_id,
        uploaded_by=context.user_id,
        filename=file.filename or "document.txt",
        content_type=file.content_type,
        content=content,
    )

    return DocumentUploadResponse(
        document_id=document_id,
        status="ready",
    )