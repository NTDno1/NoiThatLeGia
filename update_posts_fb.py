import os
import re
from bs4 import BeautifulSoup

project_dir = r"c:\Users\datt\Documents\GitProject\NoiThatLeGia"

# 1. Update Facebook links across all HTML files
html_files = []
for root, dirs, files in os.walk(project_dir):
    for f in files:
        if f.endswith(".html"):
            html_files.append(os.path.join(root, f))

for file_path in html_files:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace facebook links
        new_content = content.replace("https://www.facebook.com/noithatlegiah", "https://www.facebook.com/noithatlegiahn")
        
        # If it's gioi-thieu/index.html, add the 3 posts
        if file_path.endswith(r"gioi-thieu\index.html"):
            soup = BeautifulSoup(new_content, 'html.parser')
            wrap_blg = soup.find('div', class_='wrap_blg')
            if wrap_blg:
                new_html = """
<div class="blog-item-thumbnail">
<a class="d-block img1" href="javascript:void(0);"><img alt="TIÊU CHUẨN CHẤT LƯỢNG" src="../upload/new/gioi_thieu_4.png"/></a>
<section>
<p class="meta">21 tháng 07, 2021</p>
<h3><a href="javascript:void(0);">TIÊU CHUẨN CHẤT LƯỢNG</a></h3>
<p class="summary">Áp dụng các hệ thống tiêu chuẩn quản lý chất lượng khắt khe nhất, Lê Gia cam kết mọi dự án đều đạt chất lượng hoàn hảo, an toàn tuyệt đối và bền vững cùng thời gian.</p>
<a class="readmore" href="javascript:void(0);"><span>Xem thêm</span><i class="fas fa-arrow-right"></i></a>
</section>
</div>
<div class="blog-item-thumbnail">
<a class="d-block img1" href="javascript:void(0);"><img alt="ĐỐI TÁC CHIẾN LƯỢC" src="../upload/new/gioi_thieu_5.png"/></a>
<section>
<p class="meta">22 tháng 07, 2021</p>
<h3><a href="javascript:void(0);">ĐỐI TÁC CHIẾN LƯỢC</a></h3>
<p class="summary">Chúng tôi tự hào hợp tác với các nhà cung cấp vật liệu và đối tác công nghệ hàng đầu, đảm bảo nguồn lực vững chắc để thực hiện các siêu dự án quy mô lớn.</p>
<a class="readmore" href="javascript:void(0);"><span>Xem thêm</span><i class="fas fa-arrow-right"></i></a>
</section>
</div>
<div class="blog-item-thumbnail">
<a class="d-block img1" href="javascript:void(0);"><img alt="VĂN HÓA DOANH NGHIỆP" src="../upload/new/gioi_thieu_6.png"/></a>
<section>
<p class="meta">23 tháng 07, 2021</p>
<h3><a href="javascript:void(0);">VĂN HÓA DOANH NGHIỆP</a></h3>
<p class="summary">Môi trường làm việc năng động, sáng tạo và đoàn kết. Lê Gia luôn coi trọng con người là tài sản quý giá nhất để phát triển bền vững và vươn xa hơn nữa.</p>
<a class="readmore" href="javascript:void(0);"><span>Xem thêm</span><i class="fas fa-arrow-right"></i></a>
</section>
</div>"""
                wrap_blg.append(BeautifulSoup(new_html, 'html.parser'))
                new_content = str(soup)

        # If it's dich-vu/index.html, add the 3 posts
        elif file_path.endswith(r"dich-vu\index.html"):
            soup = BeautifulSoup(new_content, 'html.parser')
            wrap_blg = soup.find('div', class_='wrap_blg')
            if wrap_blg:
                new_html = """
<div class="blog-item-thumbnail">
<a class="d-block img1" href="javascript:void(0);"><img alt="THIẾT KẾ NỘI THẤT CAO CẤP" src="../upload/new/dich_vu_4.png"/></a>
<section>
<p class="meta">21 tháng 07, 2021</p>
<h3><a href="javascript:void(0);">THIẾT KẾ NỘI THẤT CAO CẤP</a></h3>
<p class="summary">Kiến tạo không gian sống đẳng cấp, sang trọng. Sự kết hợp hoàn hảo giữa thẩm mỹ nghệ thuật và công năng sử dụng thực tế cho căn hộ, biệt thự cao cấp.</p>
<a class="readmore" href="javascript:void(0);"><span>Xem thêm</span><i class="fas fa-arrow-right"></i></a>
</section>
</div>
<div class="blog-item-thumbnail">
<a class="d-block img1" href="javascript:void(0);"><img alt="THI CÔNG HẠ TẦNG KỸ THUẬT" src="../upload/new/dich_vu_5.png"/></a>
<section>
<p class="meta">22 tháng 07, 2021</p>
<h3><a href="javascript:void(0);">THI CÔNG HẠ TẦNG KỸ THUẬT</a></h3>
<p class="summary">Cung cấp giải pháp thi công hạ tầng giao thông, hệ thống cấp thoát nước và san lấp mặt bằng đạt chuẩn quốc gia cho các dự án bất động sản lớn.</p>
<a class="readmore" href="javascript:void(0);"><span>Xem thêm</span><i class="fas fa-arrow-right"></i></a>
</section>
</div>
<div class="blog-item-thumbnail">
<a class="d-block img1" href="javascript:void(0);"><img alt="TƯ VẤN QUẢN LÝ DỰ ÁN" src="../upload/new/dich_vu_6.png"/></a>
<section>
<p class="meta">23 tháng 07, 2021</p>
<h3><a href="javascript:void(0);">TƯ VẤN QUẢN LÝ DỰ ÁN</a></h3>
<p class="summary">Đội ngũ chuyên gia giàu kinh nghiệm của Lê Gia sẽ trực tiếp quản lý, giám sát rủi ro và tối ưu hóa chi phí đầu tư cho chủ đầu tư một cách chuyên nghiệp nhất.</p>
<a class="readmore" href="javascript:void(0);"><span>Xem thêm</span><i class="fas fa-arrow-right"></i></a>
</section>
</div>"""
                wrap_blg.append(BeautifulSoup(new_html, 'html.parser'))
                new_content = str(soup)

        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
                
    except Exception as e:
        print(f"Error on {file_path}: {e}")
