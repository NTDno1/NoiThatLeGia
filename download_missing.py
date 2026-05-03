# -*- coding: utf-8 -*-
"""
Tai them hinh anh con thieu (thumbs, upload)
"""

import os
import re
import requests
from urllib.parse import urljoin, urlparse, unquote

BASE_URL = "https://legiaconstruction.com/"
OUTPUT_DIR = "legiaconstruction_local"
session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
})

def url_to_path(url):
    """Chuyen URL thanh duong dan file local"""
    parsed = urlparse(url)
    path = unquote(parsed.path).strip('/')
    if not path:
        return None
    return os.path.join(OUTPUT_DIR, path)

def download_resource(url):
    """Tai tai nguyen ve local"""
    try:
        response = session.get(url, timeout=15, stream=True)
        if response.status_code == 200:
            filepath = url_to_path(url)
            if filepath:
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content(8192):
                        f.write(chunk)
                print(f"  [+] {filepath}")
                return True
    except Exception as e:
        print(f"  [!] Loi: {url} - {e}")
    return False

def collect_missing_resources():
    """Tim va tai cac tai nguyen con thieu"""
    print("Dang quet cac file HTML de tim tai nguyen con thieu...")

    missing = set()
    processed = set()

    for root, dirs, files in os.walk(OUTPUT_DIR):
        for filename in files:
            if filename.endswith('.html'):
                filepath = os.path.join(root, filename)
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                # Tim tat ca src va href
                patterns = [
                    r'src=["\']([^"\']+)["\']',
                    r'href=["\']([^"\']+)["\']',
                    r'url\(["\']?([^"\'()]+)["\']?\)',
                ]

                for pattern in patterns:
                    for match in re.finditer(pattern, content):
                        url = match.group(1)
                        if url.startswith('http') and 'legiaconstruction.com' in url:
                            if url not in processed:
                                processed.add(url)
                                filepath = url_to_path(url)
                                if filepath and not os.path.exists(filepath):
                                    missing.add((url, filepath))

    print(f"TIM THAY {len(missing)} tai nguyen con thieu")

    downloaded = 0
    for url, path in missing:
        if download_resource(url):
            downloaded += 1

    print(f"Da tai {downloaded} tai nguyen")

if __name__ == '__main__':
    collect_missing_resources()
