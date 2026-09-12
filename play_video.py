"""使用 OpenCV 播放 video 資料夾中的影片。"""

from __future__ import annotations

import argparse
from pathlib import Path

import cv2


VIDEO_EXTENSIONS = {".avi", ".mkv", ".mov", ".mp4", ".webm"}
VIDEO_DIRECTORY = Path(__file__).parent / "video"
WINDOW_NAME = "OpenCV 影片播放器"


def find_video(video_name: str | None) -> Path:
    """取得指定影片，或回傳 video 資料夾中的第一支影片。"""
    if video_name:
        video_path = VIDEO_DIRECTORY / video_name
        if not video_path.is_file():
            raise FileNotFoundError(f"找不到影片：{video_path}")
        return video_path

    video_paths = sorted(
        path
        for path in VIDEO_DIRECTORY.iterdir()
        if path.is_file() and path.suffix.lower() in VIDEO_EXTENSIONS
    )
    if not video_paths:
        raise FileNotFoundError(f"{VIDEO_DIRECTORY} 中沒有影片檔。")
    return video_paths[0]


def play_video(video_path: Path) -> int:
    """播放指定影片，按 q 或 Esc 結束。"""
    url="https://tcnvr6.taichung.gov.tw/bdbf9365"
    capture = cv2.VideoCapture(url)
    if not capture.isOpened():
        print(f"無法開啟影片：{video_path}")
        return 1

    fps = capture.get(cv2.CAP_PROP_FPS)
    delay = max(1, round(1000 / fps)) if fps > 0 else 33

    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(WINDOW_NAME, 1280, 720)
    print(f"正在播放：{video_path.name}")
    print("按 q 或 Esc 結束播放。")

    try:
        while True:
            success, frame = capture.read()
            if not success:
                break

            cv2.imshow(WINDOW_NAME, frame)
            key = cv2.waitKey(delay) & 0xFF
            if key in (ord("q"), 27):
                break
    finally:
        capture.release()
        cv2.destroyAllWindows()

    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="使用 OpenCV 播放 video 資料夾中的影片")
    parser.add_argument("--video", help="要播放的影片檔名，例如 empty_sunny_blue_beach.mp4")
    args = parser.parse_args()

    try:
        video_path = find_video(args.video)
    except (FileNotFoundError, OSError) as error:
        print(error)
        return 1

    return play_video(video_path)


if __name__ == "__main__":
    raise SystemExit(main())