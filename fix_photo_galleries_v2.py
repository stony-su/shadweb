#!/usr/bin/env python3
import os
import re
from pathlib import Path

def fix_photo_gallery_file(file_path):
    """Fix common issues in photo gallery HTML files."""
    print(f"Fixing {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the script section and replace it with a clean version
    script_start = content.find('<script>')
    script_end = content.find('</script>')
    
    if script_start != -1 and script_end != -1:
        # Extract the photo data array
        photos_match = re.search(r'const photos = \[(.*?)\];', content, re.DOTALL)
        if photos_match:
            photos_data = photos_match.group(1)
            
            # Create clean script content
            clean_script = f'''    <script>
        // Photo data for {file_path.stem}
        const photos = [{photos_data}];
        
        let loadedImages = new Set();
        let currentModalIndex = 0;
        let currentBatch = 0;
        const batchSize = 6; // Load 6 images at a time

        // Modal functionality
        const modal = document.getElementById('photo-modal');
        const modalImage = document.getElementById('modal-image');
        const modalClose = document.getElementById('modal-close');
        const modalPrev = document.getElementById('modal-prev');
        const modalNext = document.getElementById('modal-next');
        const modalInfo = document.getElementById('modal-info');

        function openModal(index) {{
            currentModalIndex = index;
            modalImage.src = photos[index].src;
            modalImage.alt = photos[index].alt;
            modalInfo.textContent = `${{index + 1}} of ${{photos.length}}`;
            modal.style.display = 'block';
            document.body.style.overflow = 'hidden';
        }}

        function closeModal() {{
            modal.style.display = 'none';
            document.body.style.overflow = 'auto';
        }}

        function showPrevImage() {{
            currentModalIndex = (currentModalIndex - 1 + photos.length) % photos.length;
            openModal(currentModalIndex);
        }}

        function showNextImage() {{
            currentModalIndex = (currentModalIndex + 1) % photos.length;
            openModal(currentModalIndex);
        }}

        // Event listeners for modal
        modalClose.addEventListener('click', closeModal);
        modalPrev.addEventListener('click', showPrevImage);
        modalNext.addEventListener('click', showNextImage);

        // Close modal when clicking outside the image
        modal.addEventListener('click', function(e) {{
            if (e.target === modal) {{
                closeModal();
            }}
        }});

        // Keyboard navigation
        document.addEventListener('keydown', function(e) {{
            if (modal.style.display === 'block') {{
                switch(e.key) {{
                    case 'Escape':
                        closeModal();
                        break;
                    case 'ArrowLeft':
                        showPrevImage();
                        break;
                    case 'ArrowRight':
                        showNextImage();
                        break;
                }}
            }}
        }});

        function createPhotoElement(photo, index) {{
            const photoItem = document.createElement('div');
            photoItem.className = 'photo-item loading';
            photoItem.dataset.index = index;
            
            const img = document.createElement('img');
            img.src = photo.src;
            img.alt = photo.alt;
            img.loading = 'lazy';
            
            const placeholder = document.createElement('div');
            placeholder.className = 'loading-placeholder';
            placeholder.textContent = `Loading...`;
            
            photoItem.appendChild(img);
            photoItem.appendChild(placeholder);
            
            // Add click event for modal
            photoItem.addEventListener('click', function() {{
                openModal(index);
            }});
            
            return photoItem;
        }}

        function loadNextBatch() {{
            const startIndex = currentBatch * batchSize;
            const endIndex = Math.min(startIndex + batchSize, photos.length);
            
            for (let i = startIndex; i < endIndex; i++) {{
                const photoItem = document.querySelector(`[data-index="${{i}}"]`);
                if (photoItem) {{
                    const img = photoItem.querySelector('img');
                    const placeholder = photoItem.querySelector('.loading-placeholder');
                    
                    img.onload = function() {{
                        photoItem.classList.remove('loading');
                        photoItem.classList.add('loaded');
                        placeholder.style.display = 'none';
                        loadedImages.add(i);
                        updateMemoryInfo();
                    }};
                    
                    img.onerror = function() {{
                        placeholder.textContent = 'Error loading';
                        placeholder.style.color = '#ff0000';
                    }};
                }}
            }}
            
            currentBatch++;
        }}

        function updateMemoryInfo() {{
            const memoryInfo = document.getElementById('memory-info');
            memoryInfo.textContent = `Loaded ${{loadedImages.size}} of ${{photos.length}} photos`;
        }}

        function unloadDistantImages() {{
            // Remove images that are far from viewport to save memory
            const viewportHeight = window.innerHeight;
            const photoItems = document.querySelectorAll('.photo-item');
            
            photoItems.forEach((item, index) => {{
                const rect = item.getBoundingClientRect();
                const isVisible = rect.top < viewportHeight + 200 && rect.bottom > -200;
                
                if (!isVisible && loadedImages.has(index)) {{
                    const img = item.querySelector('img');
                    img.src = ''; // Clear src to unload from memory
                    item.classList.remove('loaded');
                    item.classList.add('loading');
                    loadedImages.delete(index);
                    
                    const placeholder = item.querySelector('.loading-placeholder');
                    placeholder.style.display = 'block';
                    placeholder.textContent = 'Unloaded';
                }}
            }});
            
            updateMemoryInfo();
        }}

        // Initialize gallery
        document.addEventListener('DOMContentLoaded', function() {{
            const photoGrid = document.getElementById('photo-grid');
            
            // Create photo elements
            photos.forEach((photo, index) => {{
                const photoElement = createPhotoElement(photo, index);
                photoGrid.appendChild(photoElement);
            }});
            
            // Load first batch
            loadNextBatch();
            
            // Set up intersection observer for lazy loading
            const observer = new IntersectionObserver((entries) => {{
                entries.forEach(entry => {{
                    if (entry.isIntersecting) {{
                        const index = parseInt(entry.target.dataset.index);
                        if (!loadedImages.has(index)) {{
                            const img = entry.target.querySelector('img');
                            img.src = photos[index].src;
                        }}
                    }}
                }});
            }}, {{ rootMargin: '50px' }});
            
            // Observe all photo items
            document.querySelectorAll('.photo-item').forEach(item => {{
                observer.observe(item);
            }});
            
            // Set up scroll listener for memory management
            let scrollTimeout;
            window.addEventListener('scroll', () => {{
                clearTimeout(scrollTimeout);
                scrollTimeout = setTimeout(unloadDistantImages, 1000);
            }});
            
            // Load more batches as needed
            setInterval(() => {{
                if (currentBatch * batchSize < photos.length) {{
                    loadNextBatch();
                }}
            }}, 2000);
        }});
    </script>'''
            
            # Replace the entire script section
            content = content[:script_start] + clean_script + content[script_end + 8:]
    
    # Remove duplicate modal HTML elements
    modal_pattern = r'<!-- Photo Modal -->\s*<div id="photo-modal" class="photo-modal">\s*<div class="modal-content">\s*<span class="modal-close" id="modal-close">&times;</span>\s*<img id="modal-image" class="modal-image" src="" alt="">\s*<div class="modal-nav modal-prev" id="modal-prev">‹</div>\s*<div class="modal-nav modal-next" id="modal-next">›</div>\s*<div class="modal-info" id="modal-info"></div>\s*</div>\s*</div>'
    modals = re.findall(modal_pattern, content, re.DOTALL)
    if len(modals) > 1:
        # Keep only the first modal
        content = re.sub(modal_pattern, modals[0], content, flags=re.DOTALL)
    
    # Ensure proper HTML structure
    if not content.strip().endswith('</html>'):
        content = content.strip() + '\n</body>\n</html>'
    
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