#!/usr/bin/env python3
"""
HEIC to JPG Converter
Automatically converts all HEIC files in the Photos From Staff directory to JPG format.
"""

import os
import sys
from pathlib import Path
from PIL import Image
import pillow_heif

def convert_heic_to_jpg(input_dir):
    """
    Convert all HEIC files in the specified directory to JPG format.
    
    Args:
        input_dir (str): Path to the directory containing HEIC files
    """
    # Register HEIF opener with Pillow
    pillow_heif.register_heif_opener()
    
    # Convert to Path object for easier handling
    input_path = Path(input_dir)
    
    if not input_path.exists():
        print(f"Error: Directory '{input_dir}' does not exist.")
        return
    
    if not input_path.is_dir():
        print(f"Error: '{input_dir}' is not a directory.")
        return
    
    # Find all HEIC files
    heic_files = list(input_path.glob("*.HEIC")) + list(input_path.glob("*.heic"))
    
    if not heic_files:
        print(f"No HEIC files found in '{input_dir}'")
        return
    
    print(f"Found {len(heic_files)} HEIC files to convert...")
    
    converted_count = 0
    error_count = 0
    
    for heic_file in heic_files:
        try:
            # Create output filename (same name but .jpg extension)
            output_file = heic_file.with_suffix('.jpg')
            
            # Skip if JPG already exists
            if output_file.exists():
                print(f"Skipping {heic_file.name} - JPG already exists")
                continue
            
            print(f"Converting {heic_file.name}...")
            
            # Open and convert the image
            with Image.open(heic_file) as img:
                # Convert to RGB if necessary (HEIC might be in different color space)
                if img.mode in ('RGBA', 'LA', 'P'):
                    img = img.convert('RGB')
                
                            # Save as JPG
            img.save(output_file, 'JPEG', quality=95)
            
            # Delete the original HEIC file after successful conversion
            heic_file.unlink()
            
            converted_count += 1
            print(f"✓ Converted {heic_file.name} -> {output_file.name} (HEIC deleted)")
            
        except Exception as e:
            error_count += 1
            print(f"✗ Error converting {heic_file.name}: {str(e)}")
    
    print(f"\nConversion complete!")
    print(f"Successfully converted: {converted_count} files")
    if error_count > 0:
        print(f"Errors: {error_count} files")

def main():
    """Main function to run the converter."""
    # Default directory path
    default_dir = "pictures/Photos From Staff-20250711T010436Z-1-001/Photos From Staff"
    
    # Check if directory exists
    if not os.path.exists(default_dir):
        print(f"Error: Directory '{default_dir}' not found.")
        print("Please make sure the path is correct.")
        return
    
    print("HEIC to JPG Converter")
    print("=" * 30)
    print(f"Target directory: {default_dir}")
    print()
    
    # Ask for confirmation
    response = input("Do you want to convert all HEIC files to JPG? (y/n): ").lower().strip()
    
    if response in ['y', 'yes']:
        convert_heic_to_jpg(default_dir)
    else:
        print("Conversion cancelled.")

if __name__ == "__main__":
    main() 