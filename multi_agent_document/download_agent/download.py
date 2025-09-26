import os
import hashlib
import aiohttp


DOWNLOAD_CACHE_DIR = "downloaded_docs"
os.makedirs(DOWNLOAD_CACHE_DIR, exist_ok=True)

def get_cache_filename(url: str) -> str:
    url_hash = hashlib.sha256(url.encode("utf-8")).hexdigest()
    return os.path.join(DOWNLOAD_CACHE_DIR, f"{url_hash}.pdf")

async def download_document(url: str) -> bytes:
    cache_path = get_cache_filename(url)
    if os.path.exists(cache_path):
        with open(cache_path, "rb") as f:
            return f.read()
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            content = await resp.read()
            with open(cache_path, "wb") as f:
                f.write(content)
            return content
