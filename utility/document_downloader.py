import os
import hashlib
from urllib.parse import urlparse

import aiohttp

DOWNLOAD_CACHE_DIR = "downloaded_docs"
os.makedirs(DOWNLOAD_CACHE_DIR, exist_ok=True)

def get_cache_filename(url: str) -> str:
    parsed = urlparse(url)
    path = parsed.path
    ext = os.path.splitext(path)[1] or ".bin"  # 확장자 없으면 .bin
    url_hash = hashlib.sha256(url.encode("utf-8")).hexdigest()
    return os.path.join(DOWNLOAD_CACHE_DIR, f"{url_hash}{ext}")

async def download_document(url: str) -> bytes:
    cache_path = get_cache_filename(url)
    if os.path.exists(cache_path):
        print(f"[DEBUG] 캐시에서 로드: {cache_path}")
        with open(cache_path, "rb") as f:
            content = f.read()
        return content

    print(f"[DEBUG] 다운로드 시작: {url}")
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                raise Exception(f"다운로드 실패: {resp.status}")
            content = await resp.read()
            with open(cache_path, "wb") as f:
                f.write(content)
            print(f"[DEBUG] 다운로드 완료 및 저장: {cache_path} ({len(content)} bytes)")

            debug_pdf_path = "debug_downloaded.pdf"
            with open(debug_pdf_path, "wb") as f:
                f.write(content)
            print(f"[DEBUG] 다운로드된 PDF 저장: {debug_pdf_path}")

            return content
