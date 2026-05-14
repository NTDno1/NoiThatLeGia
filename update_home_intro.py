import re
from bs4 import BeautifulSoup

path = r'c:\Users\datt\Documents\GitProject\NoiThatLeGia\index.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

soup = BeautifulSoup(content, 'html.parser')

vctnd = soup.find('div', class_='vctnd')

if vctnd:
    new_html = """
<div class="vctnd text-left" style="text-align: left !important;">
    <h3 class="mb-4" style="font-size: 24px; color: var(--main-color, #0f4c75); font-weight: 700;">Chào mừng bạn đã đến với Lê Gia!</h3>
    <div class="row align-items-center">
        <div class="col-md-5 mb-3 mb-md-0">
            <img src="upload/new/home_intro.png" class="img-fluid rounded shadow-sm" style="border: 3px solid #fff;" alt="Giới thiệu Lê Gia">
        </div>
        <div class="col-md-7">
            <p class="text-justify mb-3" style="font-size: 15px; line-height: 1.7;">
                Chúng tôi là đội ngũ chuyên gia từng đảm nhiệm vị trí Giám đốc dự án, Chỉ huy trưởng tại các công trình trọng điểm của Tập đoàn Hòa Bình và nhiều dự án quốc tế (Lixil, Metro Line, Heineken...).
            </p>
            <p class="text-justify mb-0" style="font-size: 15px; line-height: 1.7;">
                Được sự tín nhiệm tuyệt đối từ khách hàng, <strong>CÔNG TY CỔ PHẦN XÂY DỰNG VÀ ĐẦU TƯ THƯƠNG MẠI LÊ GIA</strong> ra đời với sứ mệnh kiến tạo những công trình chất lượng, đạt chuẩn tiến độ và mang lại giá trị bền vững cho xã hội.
            </p>
        </div>
    </div>
    <div class="mt-4 p-4 rounded shadow-sm" style="background-color: #f8f9fa; border-left: 4px solid var(--main-color, #0f4c75);">
        <h4 class="mb-3" style="color: var(--main-color, #0f4c75); font-size: 18px;"><i class="fas fa-quote-left mr-2"></i>Tâm Huyết Lê Gia</h4>
        <div class="row">
            <div class="col-sm-6">
                <p class="mb-1 font-italic text-muted" style="font-size: 15px;">"Lê Gia xây dựng công trình,<br>Hoàn thành sứ mệnh hết mình tận tâm.</p>
                <p class="mb-1 font-italic text-muted" style="font-size: 15px;">Tuyệt đối không có sai lầm,<br>Công trình chất lượng xứng tầm quốc gia.</p>
            </div>
            <div class="col-sm-6">
                <p class="mb-0 font-italic text-muted" style="font-size: 15px;">Yên tâm với những ngôi nhà,<br>An toàn bền vững như là thái sơn."</p>
            </div>
        </div>
    </div>
</div>
"""
    vctnd.replace_with(BeautifulSoup(new_html, 'html.parser'))

    # Also make sure the title vctd is aligned left if it has inline center styles
    vctd = soup.find('div', class_='vctd')
    if vctd:
        vctd['style'] = vctd.get('style', '') + '; text-align: left;'

    with open(path, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print("Updated intro section in index.html")
else:
    print("Could not find vctnd")
