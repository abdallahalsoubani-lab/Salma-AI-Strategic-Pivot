"""
مسارات API للمستندات
Document API Routes
"""

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Query
from typing import List, Optional
from uuid import UUID

from app.api.dependencies import get_current_user, get_db
from app.services.documents.document_service import DocumentService

router = APIRouter(prefix="/api/documents", tags=["documents"])


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    current_user = Depends(get_current_user),
    db = Depends(get_db)
):
    """
    رفع مستند جديد
    Upload a new document
    """

    # Validate file
    max_size = 50 * 1024 * 1024  # 50MB
    content = await file.read()

    if len(content) > max_size:
        raise HTTPException(
            status_code=400,
            detail="حجم الملف يتجاوز الحد المسموح (50MB)"
        )

    service = DocumentService(db)

    document = await service.upload_document(
        user_id=current_user.id,
        filename=file.filename,
        content=content,
        mime_type=file.content_type
    )

    return {
        "id": str(document.id),
        "filename": document.original_filename,
        "status": document.status.value,
        "message": "تم رفع الملف بنجاح. جاري المعالجة..."
    }


@router.post("/{document_id}/process")
async def process_document(
    document_id: UUID,
    current_user = Depends(get_current_user),
    db = Depends(get_db)
):
    """
    معالجة المستند
    Process uploaded document (extract text, create embeddings)
    """

    service = DocumentService(db)
    document = await service.get_document(document_id)

    if not document:
        raise HTTPException(status_code=404, detail="المستند غير موجود")

    if document.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="غير مصرح")

    document = await service.process_document(document_id)

    return {
        "id": str(document.id),
        "status": document.status.value,
        "page_count": document.page_count,
        "word_count": document.word_count,
        "chunk_count": document.chunk_count,
        "language": document.language_detected,
        "error": document.processing_error
    }


@router.get("")
async def list_documents(
    current_user = Depends(get_current_user),
    db = Depends(get_db),
    limit: int = Query(50, le=100),
    offset: int = 0
):
    """
    قائمة المستندات
    List user's documents
    """

    service = DocumentService(db)
    documents = await service.list_documents(
        user_id=current_user.id,
        limit=limit,
        offset=offset
    )

    return {
        "documents": [
            {
                "id": str(d.id),
                "filename": d.original_filename,
                "type": d.document_type.value,
                "size_bytes": d.file_size_bytes,
                "status": d.status.value,
                "page_count": d.page_count,
                "chunk_count": d.chunk_count,
                "language": d.language_detected,
                "uploaded_at": d.uploaded_at.isoformat()
            }
            for d in documents
        ],
        "total": len(documents),
        "limit": limit,
        "offset": offset
    }


@router.get("/{document_id}")
async def get_document(
    document_id: UUID,
    current_user = Depends(get_current_user),
    db = Depends(get_db)
):
    """
    تفاصيل المستند
    Get document details
    """

    service = DocumentService(db)
    document = await service.get_document(document_id)

    if not document:
        raise HTTPException(status_code=404, detail="المستند غير موجود")

    if document.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="غير مصرح")

    return {
        "id": str(document.id),
        "filename": document.original_filename,
        "type": document.document_type.value,
        "mime_type": document.mime_type,
        "size_bytes": document.file_size_bytes,
        "status": document.status.value,
        "page_count": document.page_count,
        "word_count": document.word_count,
        "chunk_count": document.chunk_count,
        "language": document.language_detected,
        "title": document.title,
        "author": document.author,
        "is_embedded": document.is_embedded,
        "embedding_model": document.embedding_model,
        "metadata": document.custom_metadata,
        "processing_error": document.processing_error,
        "uploaded_at": document.uploaded_at.isoformat(),
        "processed_at": document.processing_completed_at.isoformat() if document.processing_completed_at else None
    }


@router.delete("/{document_id}")
async def delete_document(
    document_id: UUID,
    current_user = Depends(get_current_user),
    db = Depends(get_db)
):
    """
    حذف مستند
    Delete a document
    """

    service = DocumentService(db)
    document = await service.get_document(document_id)

    if not document:
        raise HTTPException(status_code=404, detail="المستند غير موجود")

    if document.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="غير مصرح")

    await service.delete_document(document_id)

    return {"message": "تم حذف المستند بنجاح"}


@router.post("/search")
async def search_documents(
    query: str,
    current_user = Depends(get_current_user),
    db = Depends(get_db),
    limit: int = Query(10, le=50),
    document_ids: Optional[List[UUID]] = None
):
    """
    البحث في المستندات
    Search documents using semantic similarity
    """

    service = DocumentService(db)

    results = await service.search_documents(
        user_id=current_user.id,
        query=query,
        limit=limit,
        document_ids=document_ids
    )

    return {
        "query": query,
        "results": results,
        "total": len(results)
    }
