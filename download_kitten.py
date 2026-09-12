"""從 Pexels 搜尋並下載一張小奶貓照片。"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from dotenv import load_dotenv


API_URL = "https://api.pexels.com/v1/search"

load_dotenv(override=True)


def search_photo(api_key: str, query: str) -> dict:
    """從 Pexels 搜尋照片並回傳第一筆結果。"""
    parameters = urlencode({"query": query, "per_page": 1, "page": 1})
    request = Request(
        f"{API_URL}?{parameters}",
        headers={"Authorization": api_key, "User-Agent": "kitten-photo-downloader/1.0"},
    )

    with urlopen(request, timeout=30) as response:
        data = json.load(response)

    photos = data.get("photos", [])
    if not photos:
        raise RuntimeError(f"Pexels 找不到符合「{query}」的照片。")
    return photos[0]


def download_photo(photo: dict, output_path: Path) -> None:
    """下載 Pexels 回傳的原始尺寸照片。"""
    source_url = photo.get("src", {}).get("original")
    if not source_url:
        raise RuntimeError("搜尋結果沒有可用的照片下載網址。")

    request = Request(source_url, headers={"User-Agent": "kitten-photo-downloader/1.0"})
    with urlopen(request, timeout=60) as response:
        output_path.write_bytes(response.read())


def main() -> int:
    parser = argparse.ArgumentParser(description="從 Pexels 下載一張小奶貓照片")
    parser.add_argument("--query", default="小奶貓", help="Pexels 搜尋關鍵字")
    parser.add_argument("--output", type=Path, default=Path("kitten.jpg"), help="輸出檔案路徑")
    args = parser.parse_args()

    api_key = os.getenv("PEXELS_API_KEY")
    if not api_key:
        print("錯誤：請先設定 PEXELS_API_KEY 環境變數。", file=sys.stderr)
        print("取得 API Key：https://www.pexels.com/api/", file=sys.stderr)
        return 1

    try:
        photo = search_photo(api_key, args.query)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        download_photo(photo, args.output)
    except (HTTPError, URLError, TimeoutError, OSError, RuntimeError) as error:
        print(f"下載失敗：{error}", file=sys.stderr)
        return 1

    print(f"已下載：{args.output.resolve()}")
    print(f"攝影師：{photo.get('photographer', '未知')}")
    print(f"Pexels 來源：{photo.get('url', '未知')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())