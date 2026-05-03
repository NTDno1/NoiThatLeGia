# -*- coding: utf-8 -*-
"""Tai tat ca file CSS/JS tu website nguon - phien ban day du"""
import os
import requests
import time
import re

BASE_URL = "https://legiaconstruction.com/"
OUTPUT_DIR = "c:\\Users\\datt\\Documents\\GitProject\\NoiThatLeGia"
REQUEST_DELAY = 0.2
REQUEST_TIMEOUT = 30

session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'text/css,*/*;q=0.1',
})

# Tat ca file can tai
FILES_TO_DOWNLOAD = [
    # CSS - day du
    "assets/css/main.css",
    "assets/css/responsive.css",
    "assets/css/style.css",
    "assets/css/all.css",
    "assets/css/animate.min.css",
    "assets/css/cart.css",
    "assets/css/starrr.css",
    "assets/bootstrap/bootstrap.css",
    "assets/fontawesome512/all.css",
    "assets/mmenu/mmenu.css",
    "assets/mmenu/mmenu.horizontalback.css",
    "assets/mmenu/mmenu.pagedim.css",
    "assets/mmenu/mmenu.themes.css",
    "assets/fancybox3/jquery.fancybox.css",
    "assets/fancybox3/jquery.fancybox.style.css",
    "assets/fancybox3/jquery.fancybox.themes.css",
    "assets/login/login.css",
    "assets/photobox/photobox.css",
    "assets/slick/slick.css",
    "assets/slick/slick-theme.css",
    "assets/slick/slick-style.css",
    "assets/simplyscroll/jquery.simplyscroll.css",
    "assets/simplyscroll/jquery.simplyscroll-style.css",
    "assets/fotorama/fotorama.css",
    "assets/fotorama/fotorama-style.css",
    "assets/magiczoomplus/magiczoomplus.css",
    "assets/datetimepicker/jquery.datetimepicker.css",
    "assets/owlcarousel2/owl.carousel.css",
    "assets/owlcarousel2/owl.theme.default.css",
    "assets/owlcarousel2/owl.theme.min.css",
    "assets/wowslider/engine1/style.css",
    "assets/wowslider/engine1/style.mod.css",
    "assets/lightbox/css/lightbox.min.css",
    "assets/simplelightbox/simplelightbox.min.css",
    # JS - day du
    "assets/js/jquery.min.js",
    "assets/js/plugins-scroll.js",
    "assets/js/paging.js",
    "assets/js/functions.js",
    "assets/js/apps.js",
    "assets/js/wow.min.js",
    "assets/js/starrr.js",
    "assets/bootstrap/bootstrap.js",
    "assets/bootstrap/bootstrap.bundle.js",
    "assets/bootstrap/bootstrap.bundle.min.js",
    "assets/mmenu/mmenu.js",
    "assets/mmenu/mmenu.pagedim.js",
    "assets/simplyscroll/jquery.simplyscroll.js",
    "assets/fancybox3/jquery.fancybox.js",
    "assets/fancybox3/jquery.fancybox.pack.js",
    "assets/fancybox3/jquery.fancybox.thumbs.js",
    "assets/fancybox3/jquery.fancybox.babel.js",
    "assets/fancybox3/jquery.fancybox.compat.js",
    "assets/photobox/photobox.js",
    "assets/slick/slick.js",
    "assets/owlcarousel2/owl.carousel.js",
    "assets/magiczoomplus/magiczoomplus.js",
    "assets/lightbox/js/lightbox.min.js",
    "assets/simplelightbox/simple-lightbox.min.js",
    "assets/wowslider/engine1/jquery.js",
    "assets/wowslider/engine1/wowslider.js",
    "assets/wowslider/engine1/script.js",
    # Fonts
    "assets/fontawesome512/all.min.css",
    "assets/fontawesome512/attribution.js",
    "assets/fontawesome512/brands.min.css",
    "assets/fontawesome512/fontawesome.min.css",
    "assets/fontawesome512/regular.min.css",
    "assets/fontawesome512/solid.min.css",
    "assets/fontawesome512/svg-with-js/fa.all.min.js",
    "assets/fontawesome512/svg-with-js/fa.brands.min.js",
    "assets/fontawesome512/svg-with-js/fa.fontawesome.min.js",
    "assets/fontawesome512/svg-with-js/fa.regular.min.js",
    "assets/fontawesome512/svg-with-js/fa.solid.min.js",
    "assets/fontawesome512/svg-with-js/fa-v4-font-face.min.css",
    "assets/fontawesome512/svg-with-js/fa-v4-shims.min.js",
    "assets/fontawesome512/svg-with-js/fa.all.min.js",
    "assets/fontawesome512/svg-with-js/svg-with-js.min.js",
]


def download_file(relative_path):
    """Tai mot file ve local"""
    url = BASE_URL + relative_path
    local_path = os.path.join(OUTPUT_DIR, relative_path)

    try:
        time.sleep(REQUEST_DELAY)
        response = session.get(url, timeout=REQUEST_TIMEOUT)
        if response.status_code == 200:
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            with open(local_path, 'wb') as f:
                f.write(response.content)
            size = len(response.content)
            print(f"  [+] {relative_path} ({size:,} bytes)")
            return True
        else:
            print(f"  [!] {relative_path} - HTTP {response.status_code}")
    except Exception as e:
        print(f"  [!] {relative_path} - {e}")
    return False


def main():
    print("=" * 60)
    print("TAI FILE CSS/JS/FONTS - PHIEN BAN DAY DU")
    print("=" * 60)

    success = 0
    for f in FILES_TO_DOWNLOAD:
        if download_file(f):
            success += 1

    print("\n" + "=" * 60)
    print(f"HOAN TAT: {success}/{len(FILES_TO_DOWNLOAD)} file")
    print("=" * 60)


if __name__ == '__main__':
    main()
