# -*- coding: utf-8 -*-
"""Sua duong dan ./assets/ thanh ../assets/ cho cac trang con"""
import os
import re

OUTPUT_DIR = r"c:\Users\datt\Documents\GitProject\NoiThatLeGia"


def fix_subpage(html_path):
    """Sua duong dan trong trang con"""
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Kiem tra trang nam o thu muc con (1 cap)
    rel_path = os.path.relpath(html_path, OUTPUT_DIR)
    depth = rel_path.count(os.sep)

    if depth == 1 and rel_path.endswith('index.html'):
        # Day la trang con 1 cap - sua ./ thanh ../
        # Chu y: chi sua nhung duong dan bat dau bang ./
        # Khong sua duong dan bat dau bang http:// hoac ./

        # Sua href="./... thanh href="../..."
        content = re.sub(r'href="\./(assets/|upload/|thumbs/|watermark/)', r'href="../\1', content)
        # Sua src="./... thanh src="../..."
        content = re.sub(r'src="\./(assets/|upload/|thumbs/|watermark/)', r'src="../\1', content)

    if content != original:
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


def main():
    print("=" * 60)
    print("SUA DUONG DAN CHO CAC TRANG CON")
    print("=" * 60)

    fixed = 0
    skipped = 0

    for root, dirs, files in os.walk(OUTPUT_DIR):
        for f in files:
            if f == 'index.html':
                html_path = os.path.join(root, f)
                if fix_subpage(html_path):
                    rel = os.path.relpath(html_path, OUTPUT_DIR)
                    print(f"  [OK] {rel}")
                    fixed += 1
                else:
                    skipped += 1

    print("\n" + "=" * 60)
    print(f"HOAN TAT: {fixed} trang da sua, {skipped} trang goc duoc giu nguyen")
    print("=" * 60)


if __name__ == '__main__':
    main()
