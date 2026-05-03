# -*- coding: utf-8 -*-
"""
Chuyen doi file PHP sang HTML va cap nhat duong dan link
"""

import os
import re

OUTPUT_DIR = "legiaconstruction_local"

def convert_php_to_html():
    """Duyet va chuyen doi tat ca file .php thanh .html"""

    converted = 0
    total_files = 0

    for root, dirs, files in os.walk(OUTPUT_DIR):
        for filename in files:
            total_files += 1

            if filename.endswith('.php'):
                filepath = os.path.join(root, filename)

                # Doc noi dung PHP
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                # Tao file .html cung ten
                html_path = filepath.replace('.php', '.html')
                with open(html_path, 'w', encoding='utf-8') as f:
                    f.write(content)

                # Xoa file PHP goc
                os.remove(filepath)
                converted += 1
                print(f"  [->] {filepath} -> {html_path}")

    print(f"\nDa chuyen doi {converted} file PHP thanh HTML")
    return converted

def update_links_in_files():
    """Cap nhat duong dan link trong tat ca file .html"""

    updated = 0

    for root, dirs, files in os.walk(OUTPUT_DIR):
        for filename in files:
            if filename.endswith('.html'):
                filepath = os.path.join(root, filename)

                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                original = content

                # Thay .php thanh .html trong cac thuoc tinh href, src, action
                content = re.sub(r'\.php([?#"])', r'.html\1', content)

                # Thay duong dan / thanh ./
                # Khong can thay doi vi da xu ly trong script clone

                if content != original:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    updated += 1

    print(f"Da cap nhat link trong {updated} file")
    return updated

def copy_index_to_root():
    """Sao chep index.html vao thu muc goc neu chua co"""

    index_path = os.path.join(OUTPUT_DIR, 'index.html')
    if not os.path.exists(index_path):
        # Tim file index.html dau tien
        for root, dirs, files in os.walk(OUTPUT_DIR):
            for filename in files:
                if filename == 'index.html' and root != OUTPUT_DIR:
                    src = os.path.join(root, filename)
                    import shutil
                    shutil.copy(src, index_path)
                    print(f"  [+] Da sao chep index.html vao thu muc goc")
                    return
            for filename in files:
                if filename.endswith('.html') and 'index' in filename.lower():
                    src = os.path.join(root, filename)
                    import shutil
                    shutil.copy(src, index_path)
                    print(f"  [+] Da sao chep {filename} thanh index.html o thu muc goc")
                    return

def main():
    print("=" * 50)
    print("CHUYEN DOI PHP SANG HTML")
    print("=" * 50)

    converted = convert_php_to_html()
    updated = update_links_in_files()
    copy_index_to_root()

    print("\n" + "=" * 50)
    print("HOAN TAT CHUYEN DOI!")
    print(f"- Da chuyen doi: {converted} file")
    print(f"- Da cap nhat link: {updated} file")
    print("=" * 50)

if __name__ == '__main__':
    main()
