# Tai hinh anh bang PowerShell
$headers = @{
    'User-Agent' = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    'Referer' = 'https://legiaconstruction.com/'
}
$baseUrl = "https://legiaconstruction.com/"
$outputDir = "c:\Users\datt\Documents\GitProject\NoiThatLeGia"

$images = @(
    "upload/photo/slider-moi-1752.jpg",
    "upload/photo/slider1-5086.jpg",
    "upload/photo/logo-2438.png",
    "upload/photo/3e109cd6-e7da-4fbf-86e0-6ea62f9b2a72-4086.jpeg",
    "upload/photo/mxh1-1451.png",
    "upload/photo/mxh2-3435.png",
    "upload/photo/mxh3-6287.png",
    "upload/photo/mxh4-6476.png",
    "upload/news/gt-3471.jpg",
    "upload/news/vision-9776.jpg",
    "upload/news/giam-sat-cong-trinh-la-gi-01-3690.jpg",
    "upload/news/tu-van-thiet-ke-co-dien-lanh-thuan-phat-2241.gif",
    "upload/news/thi-cong-nghiem-thu2-4890.jpg",
    "upload/news/xd-nha-6961.jpg",
    "upload/news/cap-thoat-nuoc-9253.jpg",
    "upload/news/ic1-9587.png",
    "upload/news/ic2-6299.png",
    "upload/news/ic3-5378.png",
    "upload/news/sai-lam-can-tranh-khi-xay-nha-1-4814.jpeg",
    "upload/news/cach-giam-sat-cong-trinh-xay-dung-5056.png",
    "upload/news/thiet-ke-gieng-troi-cho-nha-ong-3-4894.jpg",
    "upload/news/xu-ly-vet-nut-be-tong-1-7565.jpg",
    "upload/news/be-xln-5120.jpg",
    "upload/news/logo2-8015.png"
)

# Tao thu muc
New-Item -ItemType Directory -Path "$outputDir\upload\photo" -Force | Out-Null
New-Item -ItemType Directory -Path "$outputDir\upload\news" -Force | Out-Null
New-Item -ItemType Directory -Path "$outputDir\thumbs\1366x489x1\upload\photo" -Force | Out-Null
New-Item -ItemType Directory -Path "$outputDir\thumbs\209x241x1\upload\news" -Force | Out-Null
New-Item -ItemType Directory -Path "$outputDir\thumbs\297x359x1\upload\news" -Force | Out-Null

Write-Host "Tai hinh anh..."
$success = 0
$fail = 0

foreach ($img in $images) {
    $url = $baseUrl + $img
    $filename = Split-Path $img -Leaf
    $localPath = Join-Path $outputDir "upload\$filename"

    try {
        $response = Invoke-WebRequest -Uri $url -Headers $headers -UseBasicParsing -TimeoutSec 30
        if ($response.StatusCode -eq 200 -and $response.Content.Length -gt 100) {
            [System.IO.File]::WriteAllBytes($localPath, $response.Content)
            Write-Host "[OK] $filename ($($response.Content.Length) bytes)"
            $success++
        } else {
            Write-Host "[FAIL] $url - HTTP $($response.StatusCode)"
            $fail++
        }
    } catch {
        Write-Host "[ERROR] $filename - $_"
        $fail++
    }
    Start-Sleep -Milliseconds 100
}

Write-Host ""
Write-Host "Hoan tat: $success thanh cong, $fail that bai"
