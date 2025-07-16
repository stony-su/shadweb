#!/usr/bin/env python3
import os
import re
from pathlib import Path

def fix_photo_gallery_file(file_path):
    """Fix common issues in photo gallery HTML files."""
    print(f"Fixing {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix 1: Add missing closing braces in event listeners
    content = re.sub(
        r'if \(e\.target === modal\) \{\s*closeModal\(\);\s*\);',
        'if (e.target === modal) {\n                closeModal();\n            }\n        });',
        content
    )
    
    content = re.sub(
        r'switch\(e\.key\) \{\s*case \'Escape\':\s*closeModal\(\);\s*break;\s*case \'ArrowLeft\':\s*showPrevImage\(\);\s*break;\s*case \'ArrowRight\':\s*showNextImage\(\);\s*break;\s*\}\s*\);',
        'switch(e.key) {\n                    case \'Escape\':\n                        closeModal();\n                        break;\n                    case \'ArrowLeft\':\n                        showPrevImage();\n                        break;\n                    case \'ArrowRight\':\n                        showNextImage();\n                        break;\n                }\n            }\n        });',
        content
    )
    
    # Fix 2: Remove duplicate modal HTML elements
    modal_pattern = r'<!-- Photo Modal -->\s*<div id="photo-modal" class="photo-modal">\s*<div class="modal-content">\s*<span class="modal-close" id="modal-close">&times;</span>\s*<img id="modal-image" class="modal-image" src="" alt="">\s*<div class="modal-nav modal-prev" id="modal-prev">‹</div>\s*<div class="modal-nav modal-next" id="modal-next">›</div>\s*<div class="modal-info" id="modal-info"></div>\s*</div>\s*</div>'
    modals = re.findall(modal_pattern, content, re.DOTALL)
    if len(modals) > 1:
        # Keep only the first modal
        content = re.sub(modal_pattern, modals[0], content, flags=re.DOTALL)
    
    # Fix 3: Remove duplicate JavaScript code
    # Remove duplicate modal functionality
    modal_js_pattern = r'let currentModalIndex = 0;\s*// Modal functionality\s*const modal = document\.getElementById\(\'photo-modal\'\);\s*const modalImage = document\.getElementById\(\'modal-image\'\);\s*const modalClose = document\.getElementById\(\'modal-close\'\);\s*const modalPrev = document\.getElementById\(\'modal-prev\'\);\s*const modalNext = document\.getElementById\(\'modal-next\'\);\s*const modalInfo = document\.getElementById\(\'modal-info\'\);\s*function openModal\(index\) \{\s*currentModalIndex = index;\s*modalImage\.src = photos\[index\]\.src;\s*modalImage\.alt = photos\[index\]\.alt;\s*modalInfo\.textContent = `\$\{index \+ 1\} of \$\{photos\.length\}`;\s*modal\.style\.display = \'block\';\s*document\.body\.style\.overflow = \'hidden\';\s*\}\s*function closeModal\(\) \{\s*modal\.style\.display = \'none\';\s*document\.body\.style\.overflow = \'auto\';\s*\}\s*function showPrevImage\(\) \{\s*currentModalIndex = \(currentModalIndex - 1 \+ photos\.length\) % photos\.length;\s*openModal\(currentModalIndex\);\s*\}\s*function showNextImage\(\) \{\s*currentModalIndex = \(currentModalIndex \+ 1\) % photos\.length;\s*openModal\(currentModalIndex\);\s*\}\s*// Event listeners for modal\s*modalClose\.addEventListener\(\'click\', closeModal\);\s*modalPrev\.addEventListener\(\'click\', showPrevImage\);\s*modalNext\.addEventListener\(\'click\', showNextImage\);\s*// Close modal when clicking outside the image\s*modal\.addEventListener\(\'click\', function\(e\) \{\s*if \(e\.target === modal\) \{\s*closeModal\(\);\s*\}\s*\}\);\s*// Keyboard navigation\s*document\.addEventListener\(\'keydown\', function\(e\) \{\s*if \(modal\.style\.display === \'block\'\) \{\s*switch\(e\.key\) \{\s*case \'Escape\':\s*closeModal\(\);\s*break;\s*case \'ArrowLeft\':\s*showPrevImage\(\);\s*break;\s*case \'ArrowRight\':\s*showNextImage\(\);\s*break;\s*\}\s*\}\s*\}\);'
    
    # Find and remove duplicates
    matches = re.findall(modal_js_pattern, content, re.DOTALL)
    if len(matches) > 1:
        # Keep only the first occurrence
        content = re.sub(modal_js_pattern, matches[0], content, flags=re.DOTALL)
    
    # Fix 4: Remove duplicate event listener code
    duplicate_click_pattern = r'// Add click event for modal\s*photoItem\.addEventListener\(\'click\', function\(\) \{\s*openModal\(index\);\s*\}\);// Add click event for modal\s*photoItem\.addEventListener\(\'click\', function\(\) \{\s*openModal\(index\);\s*\}\);'
    content = re.sub(duplicate_click_pattern, '// Add click event for modal\n            photoItem.addEventListener(\'click\', function() {\n                openModal(index);\n            });', content)
    
    # Fix 5: Ensure proper script closing
    if not content.strip().endswith('</html>'):
        # Find the last script tag and ensure proper closing
        script_end = content.rfind('</script>')
        if script_end != -1:
            content = content[:script_end + 8] + '\n</body>\n</html>'
    
    # Write the fixed content back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Fixed {file_path}")

def main():
    """Fix all photo gallery files."""
    photo_gallery_dir = Path('photo-gallery')
    
    if not photo_gallery_dir.exists():
        print("Photo gallery directory not found!")
        return
    
    # Get all HTML files in the photo gallery directory
    html_files = list(photo_gallery_dir.glob('*.html'))
    
    print(f"Found {len(html_files)} HTML files to fix:")
    for file_path in html_files:
        print(f"  - {file_path}")
    
    # Fix each file
    for file_path in html_files:
        try:
            fix_photo_gallery_file(file_path)
        except Exception as e:
            print(f"Error fixing {file_path}: {e}")
    
    print("Finished fixing photo gallery files!")

if __name__ == "__main__":
    main() 