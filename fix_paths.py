# -*- coding: utf-8 -*-
"""Cap nhat duong dan trong HTML - bo query string"""
import re
import os

HTML_FILE = "c:\\Users\\datt\\Documents\\GitProject\\NoiThatLeGia\\index.html"

def fix_paths():
    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    original_len = len(content)

    # Thay domain
    content = re.sub(r'https?://legiaconstruction\.com/', './', content)

    # Bo query string cho duong dan assets
    content = re.sub(r'(href|src)="(\./)?assets/([^"?]+\.css)(\?[^"]*)?"', r'\1="\2assets/\3"', content)
    content = re.sub(r'(href|src)="(\./)?assets/([^"?]+\.js)(\?[^"]*)?"', r'\1="\2assets/\3"', content)
    content = re.sub(r'(href|src)="(\./)?assets/([^"?]+\.(png|jpg|jpeg|gif|svg|ico|woff|woff2|ttf))(\?[^"]*)?"', r'\1="\2assets/\3"', content)

    # Bo query string cho upload
    content = re.sub(r'(href|src)="(\./)?upload/([^"?]+\.(png|jpg|jpeg|gif|svg|ico))(\?[^"]*)?"', r'\1="\2upload/\3"', content)

    # Bo query string cho thumbs
    content = re.sub(r'(href|src)="(\./)?thumbs/([^"?]+\.(png|jpg|jpeg|gif|svg|ico))(\?[^"]*)?"', r'\1="\2thumbs/\3"', content)

    # Bo query string cho watermark
    content = re.sub(r'(href|src)="(\./)?watermark/([^"?]+\.(png|jpg|jpeg|gif))(\?[^"]*)?"', r'\1="\2watermark/\3"', content)

    # Xoa base tag
    content = re.sub(r'<base[^>]*>.*?</base>', '', content, flags=re.DOTALL | re.IGNORECASE)
    content = re.sub(r'<base[^>]*/?>', '', content, flags=re.IGNORECASE)

    # Chuyen .php thanh .html trong link
    content = re.sub(r'href="([^"]*)\.php([?#"&\'\)\s])', r'href="\1.html\2', content)

    with open(HTML_FILE, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Da cap nhat: {original_len:,} -> {len(content):,} bytes")


if __name__ == '__main__':
    fix_paths()
