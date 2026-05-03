# Tai thumbs bang PowerShell
$headers = @{
    'User-Agent' = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    'Referer' = 'https://legiaconstruction.com/'
}
$baseUrl = "https://legiaconstruction.com/"
$outputDir = "c:\Users\datt\Documents\GitProject\NoiThatLeGia"

$thumbs = @(
    "thumbs/1366x489x1/upload/photo/slider-moi-1752.jpg",
    "thumbs/1366x489x1/upload/photo/slider1-5086.jpg",
    "thumbs/209x241x1/upload/news/gt-3471.jpg",
    "thumbs/209x241x1/upload/news/vision-9776.jpg",
    "thumbs/209x241x1/upload/news/giam-sat-cong-trinh-la-gi-01-3690.jpg",
    "thumbs/297x359x1/upload/news/tu-van-thiet-ke-co-dien-lanh-thuan-phat-2241.gif",
    "thumbs/297x359x1/upload/news/thi-cong-nghiem-thu2-4890.jpg",
    "thumbs/297x359x1/upload/news/xd-nha-6961.jpg",
    "thumbs/297x359x1/upload/news/cap-thoat-nuoc-9253.jpg"
)

# Tao thu muc
New-Item -ItemType Directory -Path "$outputDir\thumbs\1366x489x1\upload\photo" -Force | Out-Null
New-Item -ItemType Directory -Path "$outputDir\thumbs\209x241x1\upload\news" -Force | Out-Null
New-Item -ItemType Directory -Path "$outputDir\thumbs\297x359x1\upload\news" -Force | Out-Null

Write-Host "Tai thumbs..."
$success = 0
$fail = 0

foreach ($thumb in $thumbs) {
    $url = $baseUrl + $thumb
    $filename = Split-Path $thumb -Leaf
    $localDir = Join-Path $outputDir (Split-Path $thumb -Parent).Replace('/', '\')
    $localPath = Join-Path $localDir $filename

    try {
        $response = Invoke-WebRequest -Uri $url -Headers $headers -UseBasicParsing -TimeoutSec 30
        if ($response.StatusCode -eq 200 -and $response.Content.Length -gt 100) {
            [System.IO.File]::WriteAllBytes($localPath, $response.Content)
            Write-Host "[OK] $thumb ($($response.Content.Length) bytes)"
            $success++
        } else {
            Write-Host "[FAIL] $url - HTTP $($response.StatusCode)"
            $fail++
        }
    } catch {
        Write-Host "[ERROR] $thumb - $_"
        $fail++
    }
    Start-Sleep -Milliseconds 100
}

Write-Host ""
Write-Host "Hoan tat: $success thanh cong, $fail that bai"
