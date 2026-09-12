"""讀取 images 資料夾中的圖片，並以獨立視窗顯示。"""

from pathlib import Path

import cv2


IMAGE_EXTENSIONS = {".bmp", ".jpeg", ".jpg", ".png", ".tif", ".tiff", ".webp"}
IMAGE_DIRECTORY = Path(__file__).parent / "images"


def main() -> int:
    image_paths = sorted(
        path
        for path in IMAGE_DIRECTORY.iterdir()
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
    )

    if not image_paths:
        print(f"找不到圖片：{IMAGE_DIRECTORY}")
        return 1

    opened_windows = 0
    for image_path in image_paths:
        image = cv2.imread(str(image_path), cv2.IMREAD_COLOR)
        if image is None:
            print(f"無法讀取圖片：{image_path}")
            continue

        window_name = f"圖片：{image_path.name}"
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.imshow(window_name, image)
        opened_windows += 1

    if opened_windows == 0:
        print("沒有成功讀取任何圖片。")
        return 1

    print("圖片已分別開啟，按任意鍵關閉所有視窗。")
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())