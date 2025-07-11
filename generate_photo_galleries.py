import os
import glob
from pathlib import Path

def get_photo_files(folder_path):
    """Get all image files from a folder"""
    image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.bmp', '*.webp']
    photos = []
    
    for ext in image_extensions:
        # Use case-insensitive pattern matching to avoid duplicates
        photos.extend(glob.glob(os.path.join(folder_path, ext), recursive=False))
        photos.extend(glob.glob(os.path.join(folder_path, ext.upper()), recursive=False))
    
    # Remove duplicates while preserving order
    seen = set()
    unique_photos = []
    for photo in photos:
        if photo not in seen:
            seen.add(photo)
            unique_photos.append(photo)
    
    return sorted(unique_photos)

def create_gallery_html(folder_name, folder_path, photos):
    """Create HTML content for a photo gallery"""
    
    # Convert folder name to display name
    display_name = folder_name.replace('_', ' ').replace('-', ' ')
    if 'Camera A' in display_name or 'Camera B' in display_name:
        # Format camera folders nicely
        parts = display_name.split()
        if len(parts) >= 3:
            date = ' '.join(parts[:2])
            camera = ' '.join(parts[2:])
            display_name = f"{date} - {camera}"
    
    # Create photo data array
    photo_data = []
    for photo_path in photos:
        filename = os.path.basename(photo_path)
        # Create a clean alt text from filename
        alt_text = filename.replace('.jpg', '').replace('.jpeg', '').replace('.png', '').replace('.gif', '').replace('.bmp', '').replace('.webp', '')
        alt_text = alt_text.replace('_', ' ').replace('-', ' ')
        
        # Create relative path from photo-gallery directory
        relative_path = os.path.join('..', 'pictures', folder_name, filename)
        photo_data.append({
            'src': relative_path.replace('\\', '/'),
            'alt': alt_text
        })
    
    # Generate HTML content
    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{display_name} - Shad Daily Photo Archive</title>
    <link rel="stylesheet" href="../styles.css">
    <link href="https://fonts.googleapis.com/css2?family=Times+New+Roman:ital,wght@0,400;0,700;1,400&family=Courier+New:wght@400;700&display=swap" rel="stylesheet">
    <style>
        .gallery-container {{
            max-width: 320px;
            margin: 0 auto;
            padding: 10px;
            margin-top: 80px;
        }}
        
        .gallery-header {{
            text-align: center;
            margin-bottom: 20px;
        }}
        
        .gallery-header h1 {{
            font-size: 16px;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        
        .gallery-header p {{
            font-size: 12px;
            color: #666;
        }}
        
        .photo-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 8px;
            margin-bottom: 20px;
        }}
        
        .photo-item {{
            position: relative;
            aspect-ratio: 1;
            background: #f0f0f0;
            border: 1px solid #ddd;
            overflow: hidden;
        }}
        
        .photo-item img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: opacity 0.3s ease;
        }}
        
        .photo-item.loading img {{
            opacity: 0;
        }}
        
        .photo-item.loaded img {{
            opacity: 1;
        }}
        
        .loading-placeholder {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 10px;
            color: #999;
            text-align: center;
        }}
        
        .back-link {{
            display: block;
            text-align: center;
            margin-top: 20px;
            padding: 8px;
            background: #1a1a1a;
            color: #fff;
            text-decoration: none;
            font-size: 10px;
            font-weight: bold;
        }}
        
        .back-link:hover {{
            background: #333;
        }}
        
        .memory-info {{
            text-align: center;
            font-size: 10px;
            color: #666;
            margin-top: 10px;
        }}
    </style>
</head>
<body>
    <header id="main-header" class="header">
        <div class="header-content">
            <div class="newspaper-title">
                <h1>SHAD DAILY</h1>
                <div class="subtitle">SHAD WATERLOO</div>
            </div>
            <div class="header-info">
                <div class="date">December 15, 2025</div>
                <div class="price">25¢</div>
            </div>
        </div>
        <nav class="nav-menu">
            <a href="../index.html#front-page">FRONT PAGE</a>
            <a href="../index.html#sNews">SHAD NEWS</a>
            <a href="../index.html#dailyQC">DAILY Q+C</a>
            <a href="../index.html#classifieds">CLASSIFIEDS</a>
            <a href="../archive.html">ARCHIVE</a>
        </nav>
    </header>

    <div class="gallery-container">
        <div class="gallery-header">
            <h1>{display_name.upper()}</h1>
            <p>Photo Collection</p>
        </div>

        <div class="photo-grid" id="photo-grid">
            <!-- Photos will be loaded dynamically -->
        </div>

        <div class="memory-info" id="memory-info">
            Loading photos...
        </div>

        <a href="../archive.html" class="back-link">← BACK TO ARCHIVE</a>
    </div>

    <script>
        // Photo data for {display_name}
        const photos = {photo_data};
        
        let loadedImages = new Set();
        let currentBatch = 0;
        const batchSize = 6; // Load 6 images at a time

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
    </script>
</body>
</html>'''
    
    return html_content

def main():
    """Generate photo gallery HTML files for all folders in pictures directory"""
    
    pictures_dir = "pictures"
    photo_gallery_dir = "photo-gallery"
    
    # Ensure photo-gallery directory exists
    os.makedirs(photo_gallery_dir, exist_ok=True)
    
    # Get all folders in pictures directory
    folders = [d for d in os.listdir(pictures_dir) if os.path.isdir(os.path.join(pictures_dir, d))]
    
    for folder in folders:
        folder_path = os.path.join(pictures_dir, folder)
        photos = get_photo_files(folder_path)
        
        if photos:  # Only create gallery if there are photos
            # Create filename for the gallery
            gallery_filename = folder.lower().replace(' ', '-').replace('_', '-')
            gallery_filename = gallery_filename.replace('camera-a', 'camera-a').replace('camera-b', 'camera-b')
            gallery_filename = gallery_filename.replace('photos-from-staff-20250711t010436z-1-001', 'photos-from-staff')
            gallery_filename = gallery_filename.replace('el-photos', 'el-photos')
            
            # Handle special cases for date formatting
            if 'june 30' in gallery_filename:
                gallery_filename = gallery_filename.replace('june-30', 'june30')
            elif 'july' in gallery_filename:
                # Extract date and camera info
                if 'july 1' in gallery_filename:
                    gallery_filename = gallery_filename.replace('july-1', 'july1')
                elif 'july 2' in gallery_filename:
                    gallery_filename = gallery_filename.replace('july-2', 'july2')
                elif 'july 3' in gallery_filename:
                    gallery_filename = gallery_filename.replace('july-3', 'july3')
                elif 'july 4' in gallery_filename:
                    gallery_filename = gallery_filename.replace('july-4', 'july4')
                elif 'july 5' in gallery_filename:
                    gallery_filename = gallery_filename.replace('july-5', 'july5')
                elif 'july 6' in gallery_filename:
                    gallery_filename = gallery_filename.replace('july-6', 'july6')
                elif 'july 7' in gallery_filename:
                    gallery_filename = gallery_filename.replace('july-7', 'july7')
                elif 'july 8' in gallery_filename:
                    gallery_filename = gallery_filename.replace('july-8', 'july8')
                elif 'july 9' in gallery_filename:
                    gallery_filename = gallery_filename.replace('july-9', 'july9')
            
            html_content = create_gallery_html(folder, folder_path, photos)
            
            # Write the HTML file
            output_file = os.path.join(photo_gallery_dir, f"{gallery_filename}.html")
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"Created gallery: {output_file} with {len(photos)} photos")

if __name__ == "__main__":
    main() 