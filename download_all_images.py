# -*- coding: utf-8 -*-
"""Tai thumbs va hinh anh tu cac trang con"""
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
})

# Lay danh sach file tu cac trang HTML
import re

def extract_images_from_all_html():
    """Lay tat ca hinh anh tu moi trang HTML"""
    images = {}
    html_files = []
    for root, dirs, files in os.walk(OUTPUT_DIR):
        for f in files:
            if f.endswith('.html'):
                html_files.append(os.path.join(root, f))

    for html_path in html_files:
        try:
            with open(html_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Tim tat ca src co upload hoac thumbs
            pattern = r'src="[^"]*(?:upload|thumbs)/([^"?]+\.(?:jpg|jpeg|png|gif|webp))'
            matches = re.findall(pattern, content, re.IGNORECASE)

            for m in matches:
                if isinstance(m, tuple):
                    img_path = m[0]
                else:
                    img_path = m

                # Xac dinh thu muc goc
                if 'thumbs' in img_path:
                    full_path = img_path
                else:
                    full_path = f"upload/{img_path}"

                full_path = full_path.replace('//', '/')
                images[img_path] = full_path

        except Exception as e:
            print(f"Loi doc {html_path}: {e}")

    return images


def download_image(relative_path):
    """Tai mot hinh anh"""
    # Thu tai nhieu duong dan khac nhau
    possible_paths = [
        relative_path,
        relative_path.replace('thumbs/', 'upload/'),
    ]

    # Neu la thumbs, thu tai truc tiep
    if relative_path.startswith('thumbs/'):
        url = BASE_URL + relative_path
        local_path = os.path.join(OUTPUT_DIR, relative_path)
    else:
        url = BASE_URL + "upload/" + relative_path.split('/')[-1]
        local_path = os.path.join(OUTPUT_DIR, "upload", relative_path.split('/')[-1])

    try:
        time.sleep(0.1)
        response = session.get(url, timeout=30)
        if response.status_code == 200 and len(response.content) > 100:
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            with open(local_path, 'wb') as f:
                f.write(response.content)
            return True, url, len(response.content)
        else:
            return False, url, f"HTTP {response.status_code}"
    except Exception as e:
        return False, url, str(e)[:50]


def main():
    print("=" * 60)
    print("TAI HINH ANH - TU CAC TRANG HTML")
    print("=" * 60)

    images = extract_images_from_all_html()
    print(f"\nTim thay {len(images)} hinh anh")

    # Loai bo nhung da tai roi
    already_downloaded = []
    for img_key, img_path in images.items():
        local_file = os.path.join(OUTPUT_DIR, "upload", img_key.split('/')[-1])
        thumbs_file = os.path.join(OUTPUT_DIR, img_key)
        if os.path.exists(local_file) or os.path.exists(thumbs_file):
            already_downloaded.append(img_key)

    for k in already_downloaded:
        del images[k]

    print(f"Can tai: {len(images)} hinh anh moi")

    success = 0
    fail = 0

    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(download_image, img): img for img in images.values()}
        for future in as_completed(futures):
            ok, url, info = future.result()
            if ok:
                print(f"  [+] {url.split('/')[-1]} ({info:,} bytes)")
                success += 1
            else:
                fail += 1

    print("\n" + "=" * 60)
    print(f"HOAN TAT: {success} thanh cong, {fail} that bai")
    print("=" * 60)


if __name__ == '__main__':
    main()
