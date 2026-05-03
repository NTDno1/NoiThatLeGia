# -*- coding: utf-8 -*-
"""
Clone cac trang them vao thu muc local
"""

import os
import re
import requests
from urllib.parse import urljoin, urlparse, unquote
from bs4 import BeautifulSoup
import time

# ========== CAU HINH ==========
BASE_URL = "https://legiaconstruction.com/"
OUTPUT_DIR = "legiaconstruction_local"
REQUEST_DELAY = 0.5
REQUEST_TIMEOUT = 30

session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7',
})

visited_files = set()

# Danh sach trang can clone them
PAGES_TO_CLONE = [
    "https://legiaconstruction.com/gioi-thieu",
    "https://legiaconstruction.com/dich-vu",
    "https://legiaconstruction.com/san-pham",
    "https://legiaconstruction.com/tin-tuc",
    "https://legiaconstruction.com/tuyen-dung",
    "https://legiaconstruction.com/lien-he",
]


def output_path(url):
    """Chuyen URL thanh duong dan file local"""
    parsed = urlparse(url)
    path = unquote(parsed.path).strip('/')

    if not path or path == '/':
        return os.path.join(OUTPUT_DIR, 'index.html')

    if '.' not in os.path.basename(path):
        return os.path.join(OUTPUT_DIR, path, 'index.html')

    return os.path.join(OUTPUT_DIR, path)


def ensure_dir(path):
    """Dam bao thu muc ton tai"""
    dir_path = os.path.dirname(path)
    if dir_path:
        os.makedirs(dir_path, exist_ok=True)


def is_same_domain(url):
    """Kiem tra URL co cung mien"""
    try:
        parsed = urlparse(url)
        base_parsed = urlparse(BASE_URL)
        return parsed.netloc == base_parsed.netloc or parsed.netloc == ''
    except:
        return False


def download_file(url):
    """Tai file ve local, tra ve duong dan da luu"""
    if url in visited_files:
        return output_path(url)

    try:
        response = session.get(url, timeout=REQUEST_TIMEOUT, stream=True)
        if response.status_code == 200:
            output_file = output_path(url)
            ensure_dir(output_file)

            content_type = response.headers.get('Content-Type', '')
            is_binary = 'image' in content_type or 'font' in content_type or 'octet-stream' in content_type

            mode = 'wb' if is_binary else 'w'
            encoding = None if is_binary else 'utf-8'

            with open(output_file, mode, encoding=encoding) as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            visited_files.add(url)
            print(f"  [+] File: {output_file}")
            return output_file
    except Exception as e:
        print(f"  [!] Loi tai {url}: {e}")
    return None


def download_css_resources(css_url):
    """Tai cac resource trong file CSS"""
    css_path = output_path(css_url)
    if not os.path.exists(css_path):
        return

    try:
        with open(css_path, 'r', encoding='utf-8') as f:
            css_content = f.read()

        urls = re.findall(r'url\([\'"]?([^\'")]+)[\'"]?\)', css_content)
        for res_url in urls:
            if res_url.startswith('data:'):
                continue
            absolute = urljoin(css_url, res_url)
            if is_same_domain(absolute):
                download_file(absolute)
    except Exception as e:
        print(f"  [!] Loi doc CSS: {e}")


def make_relative(target_url, current_url):
    """Chuyen URL tuyet doi thanh tuong doi"""
    target_parsed = urlparse(target_url)
    current_parsed = urlparse(current_url)

    target_path = unquote(target_parsed.path).strip('/')
    current_path = unquote(current_parsed.path).strip('/')

    if not current_path:
        return './' + (target_path if target_path else 'index.html')

    if '/' in current_path:
        current_depth = len(current_path.split('/'))
    else:
        current_depth = 0

    rel_parts = ['..'] * min(current_depth, 5) + [target_path if target_path else 'index.html']
    return './' + '/'.join(rel_parts)


def process_html(url, html_content):
    """Xu ly HTML: thay doi duong dan, tra ve cac link can tai"""
    soup = BeautifulSoup(html_content, 'lxml')
    resources_to_download = []

    # Xu ly srcset
    for img in soup.find_all('img'):
        if img.get('srcset'):
            srcset = img.get('srcset', '')
            new_srcset = []
            for item in srcset.strip().split(','):
                parts = item.strip().split()
                if parts:
                    abs_url = urljoin(url, parts[0])
                    if is_same_domain(abs_url):
                        resources_to_download.append(abs_url)
                        new_srcset.append(f"{make_relative(abs_url, url)} {parts[1]}" if len(parts) > 1 else make_relative(abs_url, url))
                    else:
                        new_srcset.append(item)
            img['srcset'] = ', '.join(new_srcset)

    # Xu ly tat ca tag co href/src
    attr_map = {
        'a': 'href', 'link': 'href', 'script': 'src',
        'img': 'src', 'source': 'src', 'video': 'src',
        'audio': 'src', 'iframe': 'src', 'form': 'action',
    }

    for tag_name, attr in attr_map.items():
        for tag in soup.find_all(tag_name):
            if not tag.get(attr):
                continue

            original = tag[attr]
            if any(original.startswith(x) for x in ['#', 'javascript:', 'mailto:', 'tel:']):
                continue

            abs_url = urljoin(url, original)

            if not is_same_domain(abs_url):
                continue

            # Loai bo query string cho kiem tra
            parsed = urlparse(abs_url)
            clean_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"

            resources_to_download.append(abs_url)

            # Chuyen doi thanh duong dan tuong doi
            rel = make_relative(abs_url, url)
            tag[attr] = rel

    # Xu ly background-image trong style
    for elem in soup.find_all(style=True):
        style = elem.get('style', '')
        new_style = re.sub(
            r'url\([\'"]?([^\'")]+)[\'"]?\)',
            lambda m: f'url({make_relative(urljoin(url, m.group(1)), url)})',
            style
        )
        elem['style'] = new_style

        # Tai resource trong style
        urls_in_style = re.findall(r'url\([\'"]?([^\'")]+)[\'"]?\)', style)
        for u in urls_in_style:
            abs_url = urljoin(url, u)
            if is_same_domain(abs_url):
                resources_to_download.append(abs_url)

    # Thay domain trong content
    result = soup.prettify('utf-8').decode('utf-8')
    result = re.sub(r'https?://legiaconstruction\.com/', './', result)
    result = re.sub(r'\.php([?#"&\'\)\s])', r'.html\1', result)

    # Loai bo base href
    result = re.sub(r'<base[^>]*>.*?</base>', '', result, flags=re.DOTALL | re.IGNORECASE)
    result = re.sub(r'<base[^>]*/?>', '', result, flags=re.IGNORECASE)

    return result, resources_to_download


def download_page(url):
    """Tai mot trang HTML"""
    try:
        time.sleep(REQUEST_DELAY)
        response = session.get(url, timeout=REQUEST_TIMEOUT)
        if response.status_code == 200:
            return response.text, response.content
    except Exception as e:
        print(f"  [!] Loi tai trang {url}: {e}")
    return None, None


def clone_page(url):
    """Clone mot trang va tai tat ca tai nguyen cua no"""
    print(f"\n[*] Dang clone: {url}")

    html_content, _ = download_page(url)
    if not html_content:
        print(f"  [!] Khong tai duoc trang")
        return

    processed_html, all_resources = process_html(url, html_content)

    # Luu HTML
    output_file = output_path(url)
    ensure_dir(output_file)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(processed_html)
    print(f"  [+] HTML: {output_file}")

    # Lay danh sach file da co
    existing_files = set()
    for root, dirs, files in os.walk(OUTPUT_DIR):
        for fname in files:
            fpath = os.path.join(root, fname)
            existing_files.add(os.path.abspath(fpath))

    # Tai cac tai nguyen (loc trung)
    downloaded_css = set()
    for res_url in all_resources:
        if res_url in visited_files:
            continue

        parsed = urlparse(res_url)
        path = unquote(parsed.path).strip('/')
        ext = os.path.splitext(path)[1].lower()

        # Tai ngay cac static resource
        if ext in ['.css', '.js', '.jpg', '.jpeg', '.png', '.gif', '.svg', '.ico', '.webp', '.woff', '.woff2', '.ttf']:
            result = download_file(res_url)
            if result and ext == '.css':
                download_css_resources(res_url)
            continue

        # Neu la HTML, tai HTML roi xu ly tiep
        if not ext or ext not in ['.jpg', '.png', '.gif', '.css', '.js', '.svg', '.ico', '.webp', '.woff', '.woff2', '.ttf', '.eot', '.pdf']:
            result = download_file(res_url)
            if result:
                # Doc va xu ly HTML moi
                try:
                    with open(result, 'r', encoding='utf-8', errors='ignore') as f:
                        sub_html = f.read()
                    sub_processed, sub_resources = process_html(res_url, sub_html)
                    with open(result, 'w', encoding='utf-8') as f:
                        f.write(sub_processed)
                    for sr in sub_resources:
                        if sr not in visited_files:
                            download_file(sr)
                            if urlparse(sr).path.endswith('.css'):
                                download_css_resources(sr)
                except:
                    pass

    print(f"  [OK] Hoan tat {url}")


def main():
    print("=" * 60)
    print("CLONE CAC TRANG BO SUNG")
    print("=" * 60)

    for page_url in PAGES_TO_CLONE:
        clone_page(page_url)

    print("\n" + "=" * 60)
    print("HOAN TAT CLONE CAC TRANG BO SUNG!")
    print(f"- So trang: {len(PAGES_TO_CLONE)}")
    print(f"- So file da tai: {len(visited_files)}")
    print("=" * 60)


if __name__ == '__main__':
    main()
