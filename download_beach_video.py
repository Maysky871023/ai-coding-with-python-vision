"""從 Pexels 搜尋並下載一段晴朗海邊影片。"""

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


API_URL = "https://api.pexels.com/videos/search"

load_dotenv(override=True)


def search_video(api_key: str, query: str) -> dict:
    """從 Pexels 搜尋影片並回傳第一筆結果。"""
    parameters = urlencode({"query": query, "per_page": 1, "page": 1})
    request = Request(
        f"{API_URL}?{parameters}",
        headers={"Authorization": api_key, "User-Agent": "beach-video-downloader/1.0"},
    )

    with urlopen(request, timeout=30) as response:
        data = json.load(response)

    videos = data.get("videos", [])
    if not videos:
        raise RuntimeError(f"Pexels 找不到符合「{query}」的影片。")
    return videos[0]


def select_video_file(video: dict) -> dict:
    """選擇最高畫質且有下載連結的影片檔案。"""
    video_files = [item for item in video.get("video_files", []) if item.get("link")]
    if not video_files:
        raise RuntimeError("搜尋結果沒有可用的影片下載連結。")

    return max(video_files, key=lambda item: item.get("width", 0) * item.get("height", 0))


def download_video(video_file: dict, output_path: Path) -> None:
    """下載影片檔案。"""
    request = Request(
        video_file["link"],
        headers={"User-Agent": "beach-video-downloader/1.0"},
    )
    with urlopen(request, timeout=120) as response:
        output_path.write_bytes(response.read())


def main() -> int:
    parser = argparse.ArgumentParser(description="從 Pexels 下載一段晴朗海邊影片")
    parser.add_argument("--query", default="sunny beach", help="Pexels 搜尋關鍵字")
    parser.add_argument("--output", type=Path, default=Path("sunny_beach.mp4"), help="輸出檔案路徑")
    args = parser.parse_args()

    api_key = os.getenv("PEXELS_API_KEY")
    if not api_key:
        print("錯誤：請先設定 PEXELS_API_KEY 環境變數。", file=sys.stderr)
        print("取得 API Key：https://www.pexels.com/api/", file=sys.stderr)
        return 1

    try:
        video = search_video(api_key, args.query)
        video_file = select_video_file(video)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        download_video(video_file, args.output)
    except (HTTPError, URLError, TimeoutError, OSError, RuntimeError) as error:
        print(f"下載失敗：{error}", file=sys.stderr)
        return 1

    print(f"已下載：{args.output.resolve()}")
    print(f"影片尺寸：{video_file.get('width')}x{video_file.get('height')}")
    print(f"Pexels 來源：https://www.pexels.com/video/{video.get('id')}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())