# -*- coding: utf-8 -*-
"""Tai lai trang chu index.html"""
import requests
import os
import re
from urllib.parse import urljoin, urlparse, unquote
from bs4 import BeautifulSoup
import time

BASE_URL = "https://legiaconstruction.com/"
OUTPUT_DIR = "legiaconstruction_local"
session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
})

def is_same_domain(url):
    try:
        p = urlparse(url)
        return p.netloc == urlparse(BASE_URL).netloc or p.netloc == ''
    except:
        return False

def make_relative(target, current):
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
    soup = BeautifulSoup(html_text, 'lxml')
    resources = []

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

    result = re.sub(r'https?://legiaconstruction\.com/', './', result)
    result = re.sub(r'\.php([?#"&\'\)\s])', r'.html\1', result)
    result = re.sub(r'<base[^>]*>.*?</base>', '', result, flags=re.DOTALL | re.IGNORECASE)
    result = re.sub(r'<base[^>]*/?>', '', result, flags=re.IGNORECASE)

    return result, resources

# Tai trang chu
print("Dang tai trang chu...")
time.sleep(0.5)
resp = session.get(BASE_URL, timeout=30)
if resp.status_code == 200:
    html = resp.text
    processed, _ = process_html(html, BASE_URL)

    with open(os.path.join(OUTPUT_DIR, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(processed)
    print(f"Da luu index.html ({len(processed)} bytes)")

    # Xoa index.php cu
    php_file = os.path.join(OUTPUT_DIR, 'index.php')
    if os.path.exists(php_file):
        os.remove(php_file)
        print("Da xoa index.php cu")

    print("HOAN TAT!")
else:
    print(f"Loi HTTP {resp.status_code}")
