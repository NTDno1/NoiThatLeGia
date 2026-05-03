# Quet tat ca trang HTML va tai hinh anh con thieu
$headers = @{
    'User-Agent' = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    'Referer' = 'https://legiaconstruction.com/'
}
$baseUrl = "https://legiaconstruction.com/"
$outputDir = "c:\Users\datt\Documents\GitProject\NoiThatLeGia"

# Lay tat ca file HTML
$htmlFiles = Get-ChildItem -Path $outputDir -Recurse -Filter "*.html" -File

Write-Host "Quet $($htmlFiles.Count) trang HTML..."

$allImages = @{}
foreach ($html in $htmlFiles) {
    $content = Get-Content $html.FullName -Raw -Encoding UTF8
    # Tim tat ca duong dan image
    $matches = [regex]::Matches($content, 'src="[^"]*\.(jpg|jpeg|png|gif|webp)[^"]*"')
    foreach ($m in $matches) {
        $src = $m.Value -replace 'src="', '' -replace '"$', ''
        # Chi lay duong dan cuc bo (bat dau bang ./)
        if ($src -match '^\./upload/' -or $src -match '^\./thumbs/' -or $src -match '^\./watermark/' -or $src -match '^\./assets/') {
            # Trich xuat filename
            $cleanSrc = $src -replace '^\./', ''
            $filename = Split-Path $cleanSrc -Leaf
            $folder = Split-Path $cleanSrc -Parent
            $key = "$folder/$filename"
            if (-not $allImages.ContainsKey($key)) {
                $allImages[$key] = $cleanSrc
            }
        }
    }
}

Write-Host "Tim thay $($allImages.Count) hinh anh unique"

# Tao thu muc can thiet
$neededFolders = @(
    "upload\photo",
    "upload\news",
    "upload\product",
    "assets\images",
    "thumbs\1366x489x1\upload\photo",
    "thumbs\131x48x1\upload\photo",
    "thumbs\209x241x1\upload\news",
    "thumbs\297x359x1\upload\news",
    "thumbs\375x275x1\upload\news",
    "thumbs\400x300x1\upload\news",
    "thumbs\400x400x2\upload\product",
    "thumbs\120x77x1\upload\news",
    "thumbs\264x180x1\upload\news",
    "watermark\news\375x275x1\upload\news",
    "watermark\news\400x300x1\upload\news",
    "watermark\product\400x400x2\upload\product"
)

foreach ($folder in $neededFolders) {
    $fullPath = Join-Path $outputDir $folder
    New-Item -ItemType Directory -Path $fullPath -Force | Out-Null
}

# Tai hinh anh
Write-Host ""
Write-Host "Dang tai hinh anh..."
$success = 0
$fail = 0
$skipped = 0
$failedUrls = @()

$delayMs = 100

foreach ($key in $allImages.Keys | Sort-Object) {
    $src = $allImages[$key]
    $filename = Split-Path $src -Leaf
    $localPath = Join-Path $outputDir $src.Replace('/', '\')

    # Kiem tra da ton tai chua
    if (Test-Path $localPath) {
        $skipped++
        continue
    }

    # Tai tu server
    $url = $baseUrl + $src.Replace('\', '/')
    try {
        $response = Invoke-WebRequest -Uri $url -Headers $headers -UseBasicParsing -TimeoutSec 30
        if ($response.StatusCode -eq 200 -and $response.Content.Length -gt 100) {
            # Tao thu muc neu can
            $dir = Split-Path $localPath -Parent
            if (-not (Test-Path $dir)) {
                New-Item -ItemType Directory -Path $dir -Force | Out-Null
            }
            [System.IO.File]::WriteAllBytes($localPath, $response.Content)
            Write-Host "[OK] $src ($($response.Content.Length) bytes)"
            $success++
        } else {
            Write-Host "[FAIL] HTTP $($response.StatusCode): $src"
            $fail++
            $failedUrls += $url
        }
    } catch {
        Write-Host "[ERROR] $src"
        $fail++
        $failedUrls += $url
    }
    Start-Sleep -Milliseconds $delayMs
}

Write-Host ""
Write-Host "============================================"
Write-Host "HOAN TAT: $success tai, $skipped bo qua, $fail that bai"
Write-Host "============================================"

if ($failedUrls.Count -gt 0) {
    Write-Host ""
    Write-Host "File loi (10 dau tien):"
    $failedUrls | Select-Object -First 10 | ForEach-Object { Write-Host "  - $_" }
}
