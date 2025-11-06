from utility.document_parser import parse_document

async def parse_document_agent(content: bytes, url: str) -> str:
    print(f"[DEBUG] 파싱 시작: {url}")
    text = parse_document(content, url)
    print(f"[DEBUG] 파싱 완료, 길이: {len(text)} characters")

    debug_path = "debug_parsed_text.txt"
    with open(debug_path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"[DEBUG] 파싱된 텍스트 저장: {debug_path}")

    return text

