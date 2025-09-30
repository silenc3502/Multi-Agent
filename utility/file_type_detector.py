from documents_analysis.domain.entity.DocumentType import DocumentType


def detect_file_type(url: str) -> DocumentType:
    if url.lower().endswith(".pdf"):
        return DocumentType.PDF
    elif url.lower().endswith(".docx"):
        return DocumentType.DOCX
    elif url.lower().endswith(".html") or url.lower().endswith(".htm"):
        return DocumentType.HTML
    else:
        return DocumentType.UNKNOWN
