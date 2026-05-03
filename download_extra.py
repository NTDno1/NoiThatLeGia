# -*- coding: utf-8 -*-
"""
Tai trang gioi-thieu, dich-vu, san-pham, tin-tuc, tuyen-dung, lien-he
"""

import os
import re
import requests
from urllib.parse import urljoin, urlparse, unquote
from bs4 import BeautifulSoup
import time

BASE_URL = "https://legiaconstruction.com/"
OUTPUT_DIR = "legiaconstruction_local"
REQUEST_DELAY = 0.3
REQUEST_TIMEOUT = 30

session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7',
})

PAGES = [
    ("https://legiaconstruction.com/gioi-thieu", "gioi-thieu"),
    ("https://legiaconstruction.com/dich-vu", "dich-vu"),
    ("https://legiaconstruction.com/san-pham", "san-pham"),
    ("https://legiaconstruction.com/tin-tuc", "tin-tuc"),
    ("https://legiaconstruction.com/tuyen-dung", "tuyen-dung"),
    ("https://legiaconstruction.com/lien-he", "lien-he"),
]


def ensure_dir(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)


def is_same_domain(url):
    try:
        p = urlparse(url)
        return p.netloc == urlparse(BASE_URL).netloc or p.netloc == ''
    except:
        return False


def make_relative(target, current):
    """Chuyen URL tuyet doi thanh tuong doi"""
    tp = urlparse(target)
    cp = urlparse(current)
    tpath = unquote(tp.path).strip('/')
    cpath = unquote(cp.path).strip('/')

    if not cpath:
        return './' + (tpath if tpath else 'index.html')

    depth = len(cpath.split('/')) if '/' in cpath else 0
    parts = ['..'] * min(depth, 5) + [tpath if tpath else 'index.html']
    return './' + '/'.join(parts)


def process_html(html_text, page_url):
    """Xu ly HTML, tra ve HTML da xu ly va danh sach resource URLs"""
    soup = BeautifulSoup(html_text, 'lxml')
    resources = []

    # Xu ly srcset
    for img in soup.find_all('img'):
        if img.get('srcset'):
            srcset = img['srcset']
            new_parts = []
            for item in srcset.strip().split(','):
                parts = item.strip().split()
                if parts:
                    abs_url = urljoin(page_url, parts[0])
                    resources.append(abs_url)
                    rel = make_relative(abs_url, page_url)
                    new_parts.append(f"{rel} {parts[1]}" if len(parts) > 1 else rel)
            img['srcset'] = ', '.join(new_parts)

    # Xu ly tat ca tag co href/src
    for tag_name, attr in [('a','href'), ('link','href'), ('script','src'),
                           ('img','src'), ('source','src'), ('video','src'),
                           ('audio','src'), ('iframe','src'), ('form','action')]:
        for tag in soup.find_all(tag_name):
            val = tag.get(attr)
            if not val:
                continue
            if any(val.startswith(x) for x in ['#', 'javascript:', 'mailto:', 'tel:']):
                continue

            abs_url = urljoin(page_url, val)
            if not is_same_domain(abs_url):
                continue

            resources.append(abs_url)
            tag[attr] = make_relative(abs_url, page_url)

    # Xu ly background-image
    for elem in soup.find_all(style=True):
        style = elem['style']
        new_style = re.sub(
            r'url\([\'"]?([^\'")]+)[\'"]?\)',
            lambda m: f'url({make_relative(urljoin(page_url, m.group(1)), page_url)})',
            style
        )
        elem['style'] = new_style

        urls_in_style = re.findall(r'url\([\'"]?([^\'")]+)[\'"]?\)', style)
        for u in urls_in_style:
            resources.append(urljoin(page_url, u))

    result = soup.prettify('utf-8')
    if isinstance(result, bytes):
        result = result.decode('utf-8')

    # Thay domain
    result = re.sub(r'https?://legiaconstruction\.com/', './', result)
    result = re.sub(r'\.php([?#"&\'\)\s])', r'.html\1', result)

    # Xoa base href
    result = re.sub(r'<base[^>]*>.*?</base>', '', result, flags=re.DOTALL | re.IGNORECASE)
    result = re.sub(r'<base[^>]*/?>', '', result, flags=re.IGNORECASE)

    return result, resources


def download_file(url):
    """Tai file CSS/JS/IMG ve local"""
    try:
        time.sleep(REQUEST_DELAY)
        response = session.get(url, timeout=REQUEST_TIMEOUT, stream=True)
        if response.status_code == 200:
            ct = response.headers.get('Content-Type', '')
            is_binary = 'image' in ct or 'font' in ct or 'octet-stream' in ct or 'application' in ct

            parsed = urlparse(url)
            path = unquote(parsed.path).strip('/lstrip', '/')

            # Bo query string
            path_no_qs = path.split('?')[0]

            # Neu la .css hoac .js, luu nhu text
            if path_no_qs.endswith('.css') or path_no_qs.endswith('.js'):
                is_binary = False

            output = os.path.join(OUTPUT_DIR, path_no_qs)
            ensure_dir(output)

            with open(output, 'wb' if is_binary else 'w',
                      encoding='utf-8' if not is_binary else None) as f:
                for chunk in response.iter_content(8192):
                    f.write(chunk)
            print(f"  [+] {output}")
            return True
    except Exception as e:
        print(f"  [!] {url}: {e}")
    return False


def download_css_resources(css_path):
    """Tai resource tu file CSS"""
    if not os.path.exists(css_path):
        return
    try:
        with open(css_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        urls = re.findall(r'url\([\'"]?([^\'")]+)[\'"]?\)', content)
        for u in urls:
            if u.startswith('data:'):
                continue
            abs_url = urljoin('https://legiaconstruction.com/' + css_path.replace(OUTPUT_DIR, '').replace('\\', '/').lstrip('/'), u)
            if is_same_domain(abs_url):
                download_file(abs_url)
    except:
        pass


def main():
    print("=" * 50)
    print("TAI CAC TRANG BO SUNG")
    print("=" * 50)

    for page_url, folder in PAGES:
        print(f"\n[*] Tai: {page_url}")

        try:
            time.sleep(REQUEST_DELAY)
            resp = session.get(page_url, timeout=REQUEST_TIMEOUT)
            if resp.status_code != 200:
                print(f"  [!] HTTP {resp.status_code}")
                continue

            html = resp.text
            print(f"  [*] Da nhan {len(html)} bytes HTML")

            processed, resources = process_html(html, page_url)

            # Luu HTML
            output_html = os.path.join(OUTPUT_DIR, folder, 'index.html')
            ensure_dir(output_html)
            with open(output_html, 'w', encoding='utf-8') as f:
                f.write(processed)
            print(f"  [+] Luu: {output_html} ({len(processed)} bytes)")

            # Tai resources
            for res_url in set(resources):
                parsed = urlparse(res_url)
                path = unquote(parsed.path)
                ext = os.path.splitext(path)[1].lower()

                # Chi tai static resources
                static_exts = ['.css', '.js', '.jpg', '.jpeg', '.png', '.gif', '.svg',
                               '.ico', '.webp', '.woff', '.woff2', '.ttf', '.eot']
                if ext in static_exts:
                    download_file(res_url)
                    if ext == '.css':
                        css_path = os.path.join(OUTPUT_DIR, path.strip('/').split('?')[0])
                        download_css_resources(css_path)

        except Exception as e:
            print(f"  [!] Loi: {e}")

    print("\n" + "=" * 50)
    print("HOAN TAT!")
    print("=" * 50)


if __name__ == '__main__':
    main()
