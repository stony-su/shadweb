Write-Host "HEIC to JPG Converter Setup" -ForegroundColor Green
Write-Host "===========================" -ForegroundColor Green

Write-Host "Installing required packages..." -ForegroundColor Yellow
pip install -r requirements.txt

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error installing packages. Please make sure Python and pip are installed." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "Running HEIC to JPG converter..." -ForegroundColor Yellow
python heic_to_jpg_converter.py

Write-Host ""
Write-Host "Press Enter to exit..." -ForegroundColor Cyan
Read-Host 