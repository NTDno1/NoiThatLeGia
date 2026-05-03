# -*- coding: utf-8 -*-
"""
Script clone toan bo website ve local
Website: https://legiaconstruction.com/
"""

import os
import re
import requests
from urllib.parse import urljoin, urlparse, unquote
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# ========== CAU HINH ==========
BASE_URL = "https://legiaconstruction.com/"
OUTPUT_DIR = "legiaconstruction_local"
MAX_WORKERS = 8
REQUEST_DELAY = 0.3
REQUEST_TIMEOUT = 30
MAX_PAGES = 100

# ========== KHOI TAO ==========
session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7',
})
visited_urls = set()
visited_files = set()
pending_urls = []
all_page_urls = set()
counter = {'lock': 0, 'files': 0}

def output_path(url):
    """Chuyen doi URL thanh duong dan file local"""
    parsed = urlparse(url)
    path = unquote(parsed.path)

    if path == '/' or path == '':
        return 'index.html'

    path = path.strip('/')
    if not path:
        return 'index.html'

    # Thu muc goc
    if not path or path == '/':
        return os.path.join(OUTPUT_DIR, 'index.html')

    # Tao thu muc theo cau truc
    if '.' not in os.path.basename(path):
        if not path.endswith('/'):
            path += '/'
        return os.path.join(OUTPUT_DIR, path, 'index.html')

    return os.path.join(OUTPUT_DIR, path)


def ensure_dir(path):
    """Dam bao thu muc ton tai"""
    dir_path = os.path.dirname(path)
    if dir_path:
        os.makedirs(dir_path, exist_ok=True)


def url_to_dir(url):
    """Chuyen URL thanh thu muc (cho HTML con)"""
    parsed = urlparse(url)
    path = unquote(parsed.path).strip('/')

    if not path or path == '/':
        return ''

    parts = path.rsplit('/', 1)
    if len(parts) == 1:
        return parts[0]
    return parts[0]


def sanitize_filename(name):
    """Xoa ky tu khong hop le trong ten file"""
    name = re.sub(r'[<>:"/\\|?*]', '-', name)
    name = re.sub(r'-+', '-', name)
    return name.strip('.-')


def is_same_domain(url):
    """Kiem tra URL co cung mien voi trang chu"""
    try:
        parsed = urlparse(url)
        base_parsed = urlparse(BASE_URL)
        return parsed.netloc == base_parsed.netloc or parsed.netloc == ''
    except:
        return False


def is_static_resource(url):
    """Kiem tra URL la tai nguyen tinh (css, js, hinh anh, font)"""
    static_extensions = (
        '.css', '.js', '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg',
        '.ico', '.webp', '.woff', '.woff2', '.ttf', '.eot', '.otf',
        '.webm', '.mp4', '.webp', '.avi', '.mov', '.pdf', '.zip',
        '.svg', '.json', '.xml'
    )
    parsed = urlparse(url)
    path_lower = parsed.path.lower()
    return any(path_lower.endswith(ext) for ext in static_extensions)


def download_file(url, output_file):
    """Tai file ve local"""
    try:
        response = session.get(url, timeout=REQUEST_TIMEOUT, stream=True)
        if response.status_code == 200:
            ensure_dir(output_file)
            content_type = response.headers.get('Content-Type', '')
            is_binary = 'image' in content_type or 'font' in content_type or 'application' in content_type

            with open(output_file, 'wb' if is_binary else 'w', encoding='utf-8' if not is_binary else None) as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            counter['files'] += 1
            visited_files.add(url)
            return True
    except Exception as e:
        print(f"  [!] Loi tai file {url}: {e}")
    return False


def process_html(url, html_content):
    """Xu ly HTML: thay doi duong dan, trich xuat link"""
    soup = BeautifulSoup(html_content, 'lxml')
    found_urls = []

    # Tim tat ca link trong HTML
    for tag in soup.find_all(['a', 'link', 'script', 'img', 'source', 'video', 'audio', 'iframe', 'form']):
        attr_map = {
            'a': 'href',
            'link': 'href',
            'script': 'src',
            'img': 'src',
            'source': 'src',
            'video': 'src',
            'audio': 'src',
            'iframe': 'src',
            'form': 'action',
            'img': 'srcset',
        }

        if tag.name == 'img' and tag.get('srcset'):
            # Xu ly srcset
            srcset = tag.get('srcset', '')
            new_srcset = []
            for src_item in srcset.strip().split(','):
                parts = src_item.strip().split()
                if parts:
                    src_url = urljoin(url, parts[0])
                    if len(parts) > 1:
                        new_srcset.append(f"{make_relative_url(src_url, url)} {parts[1]}")
                    else:
                        new_srcset.append(make_relative_url(src_url, url))
            tag['srcset'] = ', '.join(new_srcset)

        attr = attr_map.get(tag.name)
        if not attr or attr not in tag.attrs:
            continue

        original_url = tag[attr]
        if not original_url or original_url.startswith('#') or original_url.startswith('javascript:') or original_url.startswith('mailto:') or original_url.startswith('tel:'):
            continue

        absolute_url = urljoin(url, original_url)

        if not is_same_domain(absolute_url):
            continue

        # Loai bo query string va fragment cho so sanh
        parsed = urlparse(absolute_url)
        clean_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
        if clean_url not in visited_urls and len(visited_urls) < MAX_PAGES:
            found_urls.append(absolute_url)

        # Chuyen doi duong dan
        relative_path = make_relative_url(absolute_url, url)
        tag[attr] = relative_path

    # Xu ly background-image trong style
    for elem in soup.find_all(style=True):
        style = elem.get('style', '')
        urls = re.findall(r'url\(["\']?([^"\'()]+)["\']?\)', style)
        for img_url in urls:
            absolute_url = urljoin(url, img_url)
            if is_same_domain(absolute_url):
                rel = make_relative_url(absolute_url, url)
                style = style.replace(img_url, rel)
        elem['style'] = style

    # Xu ly inline styles voi href/src
    for elem in soup.find_all(style=True):
        style = elem.get('style', '')
        new_style = re.sub(r'url\([\'"]?([^\'")]+)[\'"]?\)',
                          lambda m: f'url({make_relative_url(urljoin(url, m.group(1)), url)})',
                          style)
        elem['style'] = new_style

    return soup.prettify('utf-8'), found_urls


def make_relative_url(target_url, current_url):
    """Chuyen URL tu tuyet doi sang tuong doi"""
    target_parsed = urlparse(target_url)
    current_parsed = urlparse(current_url)

    # Neu la trang HTML (khong co dinh dang file), them /
    target_path = unquote(target_parsed.path).strip('/')
    current_path = unquote(current_parsed.path).strip('/')

    # Neu cung thu muc
    target_dir = target_path.rsplit('/', 1)[0] if '/' in target_path else ''
    current_dir = current_path.rsplit('/', 1)[0] if '/' in current_path else ''

    # Tinh duong dan tuong doi
    if target_dir == current_dir:
        return os.path.basename(target_path) if target_path else 'index.html'

    # Tao duong dan tuong doi
    if '/' in current_path:
        current_depth = len(current_path.split('/'))
    else:
        current_depth = 0

    rel_parts = ['..'] * min(current_depth, 3) + [target_path if target_path else 'index.html']
    result = '/'.join(rel_parts)

    # Dam bao bat dau bang .. hoac ./
    if not result.startswith('../') and not result.startswith('./') and not result.startswith('/'):
        result = './' + result

    return result


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


def extract_all_links(html_content, base_url):
    """Trich xuat tat ca link tu HTML"""
    soup = BeautifulSoup(html_content, 'lxml')
    links = []
    for tag in soup.find_all('a', href=True):
        href = tag['href']
        if href.startswith('http') and is_same_domain(href):
            links.append(href)
        elif href.startswith('/') or not href.startswith('http'):
            absolute = urljoin(base_url, href)
            if is_same_domain(absolute):
                links.append(absolute)
    return list(set(links))


def process_page(url):
    """Xu ly mot trang: tai HTML, xu ly, tai tai nguyen lien quan"""
    if url in visited_urls:
        return []
    visited_urls.add(url)

    print(f"  [*] Xu ly: {url}")
    html_content, raw_content = download_page(url)

    if not html_content:
        print(f"  [!] Khong tai duoc: {url}")
        return []

    output_file = output_path(url)
    ensure_dir(output_file)

    # Xu ly HTML
    processed_html, found_links = process_html(url, html_content)

    with open(output_file, 'wb') as f:
        f.write(processed_html)

    counter['lock'] += 1
    print(f"  [+] Da luu: {output_file} ({counter['lock']}/{MAX_PAGES} trang)")

    # Tai CSS va JS ngay lap tuc
    css_js_urls = []
    soup = BeautifulSoup(processed_html, 'lxml')

    for css in soup.find_all('link', rel='stylesheet'):
        if css.get('href'):
            css_url = urljoin(url, css['href'])
            if is_same_domain(css_url) and css_url not in visited_files:
                css_path = output_path(css_url)
                ensure_dir(css_path)
                if download_file(css_url, css_path):
                    css_js_urls.append(css_url)
                    # Tai cac resource trong CSS
                    download_css_resources(css_url, css_path)

    for script in soup.find_all('script', src=True):
        script_url = urljoin(url, script['src'])
        if is_same_domain(script_url) and script_url not in visited_files:
            script_path = output_path(script_url)
            ensure_dir(script_path)
            if download_file(script_url, script_path):
                css_js_urls.append(script_url)

    # Tai hinh anh
    for img in soup.find_all('img', src=True):
        img_url = urljoin(url, img['src'])
        if is_same_domain(img_url) and img_url not in visited_files:
            img_path = output_path(img_url)
            ensure_dir(img_path)
            download_file(img_url, img_path)

    return found_links


def download_css_resources(css_url, css_path):
    """Tai cac resource (hinh anh, font) tu file CSS"""
    try:
        with open(css_path, 'r', encoding='utf-8') as f:
            css_content = f.read()

        # Tim url() trong CSS
        urls = re.findall(r'url\([\'"]?([^\'")]+)[\'"]?\)', css_content)

        for res_url in urls:
            if res_url.startswith('data:'):
                continue
            absolute_url = urljoin(css_url, res_url)
            if is_same_domain(absolute_url):
                res_path = output_path(absolute_url)
                ensure_dir(res_path)
                download_file(absolute_url, res_path)
    except Exception as e:
        print(f"  [!] Loi doc CSS {css_path}: {e}")


def main():
    print("=" * 60)
    print("CLONE WEBSITE: legiaconstruction.com")
    print("=" * 60)

    # Tao thu muc goc
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Bat dau voi trang chu
    pending_urls = [BASE_URL]

    while pending_urls and len(visited_urls) < MAX_PAGES:
        url = pending_urls.pop(0)

        # Xu ly trang
        new_links = process_page(url)
        all_page_urls.update(new_links)

        # Them link moi vao hang doi
        for link in new_links:
            if link not in visited_urls:
                pending_urls.append(link)

        # Tranh trung lap trong pending_urls
        pending_urls = list(dict.fromkeys(pending_urls))

        print(f"\n  --- Tien do: {len(visited_urls)} trang da xu ly, {counter['files']} file tai nguyen, {len(pending_urls)} cho xu ly ---\n")

    print("\n" + "=" * 60)
    print("HOAN TAT!")
    print(f"- Tong so trang HTML: {counter['lock']}")
    print(f"- Tong so file tai nguyen: {counter['files']}")
    print(f"- Du lieu luu tai: ./{OUTPUT_DIR}/")
    print("=" * 60)

    # Tao file index.html o thu muc goc neu can
    index_file = os.path.join(OUTPUT_DIR, 'index.html')
    if not os.path.exists(index_file):
        main_html = os.path.join(OUTPUT_DIR, 'legiaconstruction.com', 'index.html')
        if os.path.exists(main_html):
            import shutil
            shutil.copy(main_html, index_file)

    print(f"\nDong y dang ky server local...")
    print(f"Mo trinh duyet va truy cap: http://localhost:8000")
    print(f"Hoac truy cap truc tiep thu muc: .\\{OUTPUT_DIR}")
    print(f"\nHoac chay: python -m http.server 8000 --directory {OUTPUT_DIR}")


if __name__ == '__main__':
    main()
