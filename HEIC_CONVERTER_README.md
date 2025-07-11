# HEIC to JPG Converter

This tool automatically converts all HEIC files in the "Photos From Staff" directory to JPG format.

## Files Included

- `heic_to_jpg_converter.py` - Main Python script
- `requirements.txt` - Python dependencies
- `convert_heic.bat` - Windows batch script (easiest to use)
- `convert_heic.ps1` - PowerShell script (alternative)
- `HEIC_CONVERTER_README.md` - This file

## Quick Start (Windows)

### Option 1: Using Batch Script (Recommended)
1. Double-click `convert_heic.bat`
2. The script will automatically install dependencies and run the converter
3. Follow the prompts to confirm conversion

### Option 2: Using PowerShell
1. Right-click `convert_heic.ps1` and select "Run with PowerShell"
2. The script will automatically install dependencies and run the converter
3. Follow the prompts to confirm conversion

## Manual Installation

If you prefer to run manually:

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the converter:**
   ```bash
   python heic_to_jpg_converter.py
   ```

## What the Script Does

1. **Scans** the directory: `pictures/Photos From Staff-20250711T010436Z-1-001/Photos From Staff`
2. **Finds** all HEIC files (both `.HEIC` and `.heic` extensions)
3. **Converts** each HEIC file to JPG format with 95% quality
4. **Deletes** the original HEIC file after successful conversion
5. **Skips** files that already have JPG versions
6. **Reports** progress and any errors

## Features

- ✅ Automatic HEIC detection
- ✅ High-quality JPG conversion (95% quality)
- ✅ Skips existing JPG files
- ✅ Error handling and reporting
- ✅ Progress tracking
- ✅ Color space conversion (RGBA → RGB)
- ✅ Automatic HEIC file deletion after conversion

## Requirements

- Python 3.6 or higher
- Internet connection (for installing packages)
- Windows 10/11 (for batch/PowerShell scripts)

## Troubleshooting

**Error: "No module named 'pillow_heif'"**
- Run: `pip install pillow-heif`

**Error: "Directory not found"**
- Make sure the path `pictures/Photos From Staff-20250711T010436Z-1-001/Photos From Staff` exists

**Error: "Permission denied"**
- Run the script as administrator or check file permissions

## Output

The script will create JPG versions of all HEIC files and automatically delete the original HEIC files after successful conversion.

Example output:
```
HEIC to JPG Converter
==============================
Target directory: pictures/Photos From Staff-20250711T010436Z-1-001/Photos From Staff

Do you want to convert all HEIC files to JPG? (y/n): y
Found 36 HEIC files to convert...
Converting IMG_6115.HEIC...
✓ Converted IMG_6115.HEIC -> IMG_6115.jpg (HEIC deleted)
Converting IMG_6114.HEIC...
✓ Converted IMG_6114.HEIC -> IMG_6114.jpg (HEIC deleted)
...

Conversion complete!
Successfully converted: 36 files
``` 