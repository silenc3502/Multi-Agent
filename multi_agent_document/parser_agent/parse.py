from utility.document_parser import parse_document

async def parse_document_agent(content: bytes, url: str) -> str:
    return parse_document(content, url)
