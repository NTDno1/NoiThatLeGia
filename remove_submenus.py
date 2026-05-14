import os
from bs4 import BeautifulSoup

project_dir = r"c:\Users\datt\Documents\GitProject\NoiThatLeGia"

html_files = []
for root, dirs, files in os.walk(project_dir):
    for f in files:
        if f.endswith(".html"):
            html_files.append(os.path.join(root, f))

for file_path in html_files:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        soup = BeautifulSoup(content, 'html.parser')
        changed = False
        
        # We only want to remove submenus in the navigation (<nav>)
        for nav in soup.find_all('nav'):
            for a in nav.find_all('a'):
                title = a.get('title')
                if title in ["Dịch vụ", "Báo giá"]:
                    # Look for a <ul> sibling in the same <li>
                    parent_li = a.find_parent('li')
                    if parent_li:
                        ul = parent_li.find('ul')
                        if ul:
                            ul.decompose()
                            changed = True
                            
        if changed:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            print(f"Removed submenus in {file_path}")
            
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
