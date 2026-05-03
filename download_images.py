# -*- coding: utf-8 -*-
"""Tai tat ca hinh anh - co referer header"""
import os
import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_URL = "https://legiaconstruction.com/"
OUTPUT_DIR = "c:\\Users\\datt\\Documents\\GitProject\\NoiThatLeGia"

session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Referer': 'https://legiaconstruction.com/',
    'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
})

IMAGE_FILES = [
    "upload/photo/logo-2438.png",
    "upload/photo/3e109cd6-e7da-4fbf-86e0-6ea62f9b2a72-4086.jpeg",
    "upload/photo/mxh1-1451.png",
    "upload/photo/mxh2-3435.png",
    "upload/photo/mxh3-6287.png",
    "upload/photo/mxh4-6476.png",
    "upload/photo/slider-moi-1752.jpg",
    "upload/photo/slider1-5086.jpg",
    "upload/news/ic1-9587.png",
    "upload/news/ic2-6299.png",
    "upload/news/ic3-5378.png",
    "upload/news/gt-3471.jpg",
    "upload/news/vision-9776.jpg",
    "upload/news/giam-sat-cong-trinh-la-gi-01-3690.jpg",
    "upload/news/tu-van-thiet-ke-co-dien-lanh-thuan-phat-2241.gif",
    "upload/news/thi-cong-nghiem-thu2-4890.jpg",
    "upload/news/xd-nha-6961.jpg",
    "upload/news/cap-thoat-nuoc-9253.jpg",
    "upload/news/sai-lam-can-tranh-khi-xay-nha-1-4814.jpeg",
    "upload/news/cach-giam-sat-cong-trinh-xay-dung-5056.png",
    "upload/news/thiet-ke-gieng-troi-cho-nha-ong-3-4894.jpg",
    "upload/news/xu-ly-vet-nut-be-tong-1-7565.jpg",
    "upload/news/be-xln-5120.jpg",
    "upload/news/logo2-8015.png",
    "upload/logo-2438.png",
    "upload/mxh1-1451.png",
    "upload/mxh2-3435.png",
    "upload/mxh3-6287.png",
    "upload/mxh4-6476.png",
    "upload/ic1-9587.png",
    "upload/ic2-6299.png",
    "upload/ic3-5378.png",
    "upload/slider-moi-1752.jpg",
    "upload/slider1-5086.jpg",
    "upload/gt-3471.jpg",
    "upload/vision-9776.jpg",
    "upload/giam-sat-cong-trinh-la-gi-01-3690.jpg",
    "upload/tu-van-thiet-ke-co-dien-lanh-thuan-phat-2241.gif",
    "upload/thi-cong-nghiem-thu2-4890.jpg",
    "upload/xd-nha-6961.jpg",
    "upload/cap-thoat-nuoc-9253.jpg",
    "upload/logo2-8015.png",
    "upload/photo/z6791566547360ff4ba293d4ef16b8e9967330dc313809-4050.jpg",
    "upload/z6373010922122892331075fa5c03688407db8d1789959-1271.jpg",
    "upload/z4787811462387711b4289a85296838eed1d31247ee8b8-4177.jpg",
    "upload/z64184181796944301dae7385c7d46eb9b74787ef3b73b-1658.jpg",
    "upload/z6418384801836efc3e451780c6ad0887d810102d06834-7263.jpg",
    "upload/z5006779413345f3ac2242ea01033a0a3d1ddf9cadf42f-3994.jpg",
]


def download_image(relative_path):
    """Tai mot hinh anh"""
    url = BASE_URL + relative_path
    local_path = os.path.join(OUTPUT_DIR, relative_path)

    try:
        time.sleep(0.1)
        response = session.get(url, timeout=30)
        if response.status_code == 200 and len(response.content) > 100:
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            with open(local_path, 'wb') as f:
                f.write(response.content)
            return True, relative_path, len(response.content)
        else:
            return False, relative_path, f"HTTP {response.status_code}"
    except Exception as e:
        return False, relative_path, str(e)[:50]


def main():
    print("=" * 60)
    print("TAI HINH ANH - CO REFERER HEADER")
    print("=" * 60)

    success = 0
    fail = 0
    failed_files = []

    # Loai bo trung lap
    unique_files = list(set(IMAGE_FILES))

    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(download_image, img): img for img in unique_files}
        for future in as_completed(futures):
            ok, path, info = future.result()
            if ok:
                print(f"  [+] {path} ({info:,} bytes)")
                success += 1
            else:
                print(f"  [!] {path} - {info}")
                fail += 1
                failed_files.append(path)

    print("\n" + "=" * 60)
    print(f"HOAN TAT: {success} thanh cong, {fail} that bai")

    if failed_files:
        print("\nFile loi:")
        for f in failed_files[:10]:
            print(f"  - {f}")

    print("=" * 60)


if __name__ == '__main__':
    main()
