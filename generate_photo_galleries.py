import os
import glob
from pathlib import Path
import json

def get_photo_files(folder_path):
    """Get all image files from a folder"""
    image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.bmp', '*.webp']
    photos = []
    for ext in image_extensions:
        photos.extend(glob.glob(os.path.join(folder_path, ext), recursive=False))
        photos.extend(glob.glob(os.path.join(folder_path, ext.upper()), recursive=False))
    seen = set()
    unique_photos = []
    for photo in photos:
        if photo not in seen:
            seen.add(photo)
            unique_photos.append(photo)
    return sorted(unique_photos)

def create_gallery_html(folder_name, photos):
    display_name = folder_name.replace('_', ' ').replace('-', ' ')
    if 'Camera A' in display_name or 'Camera B' in display_name:
        parts = display_name.split()
        if len(parts) >= 3:
            date = ' '.join(parts[:2])
            camera = ' '.join(parts[2:])
            display_name = f"{date} - {camera}"
    photo_data = []
    for photo_path in photos:
        filename = os.path.basename(photo_path)
        alt_text = os.path.splitext(filename)[0].replace('_', ' ').replace('-', ' ')
        relative_path = os.path.join('..', 'pictures', folder_name, filename).replace('\\', '/')
        photo_data.append({'src': relative_path, 'alt': alt_text})
    photo_data_json = json.dumps(photo_data, ensure_ascii=False)
    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{display_name} - Shad Daily Photo Archive</title>
    <link rel="stylesheet" href="../styles.css">
    <link href="https://fonts.googleapis.com/css2?family=Times+New+Roman:ital,wght@0,400;0,700;1,400&family=Courier+New:wght@400;700&display=swap" rel="stylesheet">
    <style>
        .gallery-container {{ max-width: 320px; margin: 0 auto; padding: 10px; margin-top: 80px; }}
        .gallery-header {{ text-align: center; margin-bottom: 20px; }}
        .gallery-header h1 {{ font-size: 16px; font-weight: bold; margin-bottom: 5px; }}
        .gallery-header p {{ font-size: 12px; color: #666; }}
        .photo-grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px; margin-bottom: 20px; }}
        .photo-item {{ position: relative; aspect-ratio: 1; background: #f0f0f0; border: 1px solid #ddd; overflow: hidden; cursor: pointer; transition: transform 0.2s ease; }}
        .photo-item:hover {{ transform: scale(1.02); }}
        .photo-item img {{ width: 100%; height: 100%; object-fit: cover; transition: opacity 0.3s ease; }}
        .photo-item.loading img {{ opacity: 0; }}
        .photo-item.loaded img {{ opacity: 1; }}
        .loading-placeholder {{ position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-size: 10px; color: #999; text-align: center; }}
        .back-link {{ display: block; text-align: center; margin-top: 20px; padding: 8px; background: #1a1a1a; color: #fff; text-decoration: none; font-size: 10px; font-weight: bold; }}
        .back-link:hover {{ background: #333; }}
        .memory-info {{ text-align: center; font-size: 10px; color: #666; margin-top: 10px; }}
        .photo-modal {{ display: none; position: fixed; z-index: 2000; left: 0; top: 0; width: 100%; height: 100%; background-color: rgba(0, 0, 0, 0.9); backdrop-filter: blur(5px); }}
        .modal-content {{ position: relative; width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; }}
        .modal-image {{ max-width: 95%; max-height: 95%; object-fit: contain; border-radius: 8px; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5); }}
        .modal-close {{ position: absolute; top: 15px; right: 15px; color: #fff; font-size: 28px; font-weight: bold; cursor: pointer; background: rgba(0, 0, 0, 0.5); border-radius: 50%; width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; transition: background-color 0.3s; }}
        .modal-close:hover {{ background: rgba(0, 0, 0, 0.8); }}
        .modal-nav {{ position: absolute; top: 50%; transform: translateY(-50%); color: #fff; font-size: 24px; font-weight: bold; cursor: pointer; background: rgba(0, 0, 0, 0.5); border-radius: 50%; width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; transition: background-color 0.3s; }}
        .modal-nav:hover {{ background: rgba(0, 0, 0, 0.8); }}
        .modal-prev {{ left: 15px; }}
        .modal-next {{ right: 15px; }}
        .modal-info {{ position: absolute; bottom: 20px; left: 50%; transform: translateX(-50%); color: #fff; background: rgba(0, 0, 0, 0.7); padding: 8px 16px; border-radius: 20px; font-size: 12px; text-align: center; }}
        @media (max-width: 480px) {{ .modal-nav {{ width: 35px; height: 35px; font-size: 20px; }} .modal-close {{ width: 35px; height: 35px; font-size: 24px; }} }}
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
        <div class="photo-grid" id="photo-grid"></div>
        <div class="memory-info" id="memory-info">Loading photos...</div>
        <a href="../archive.html" class="back-link">← BACK TO ARCHIVE</a>
    </div>
    <div id="photo-modal" class="photo-modal">
        <div class="modal-content">
            <span class="modal-close" id="modal-close">&times;</span>
            <img id="modal-image" class="modal-image" src="" alt="">
            <div class="modal-nav modal-prev" id="modal-prev">‹</div>
            <div class="modal-nav modal-next" id="modal-next">›</div>
            <div class="modal-info" id="modal-info"></div>
        </div>
    </div>
    <script>
        // Photo data for {folder_name}
        const photos = {photo_data_json};
        let loadedImages = new Set();
        let currentModalIndex = 0;
        let currentBatch = 0;
        const batchSize = 6;
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
        modalClose.addEventListener('click', closeModal);
        modalPrev.addEventListener('click', showPrevImage);
        modalNext.addEventListener('click', showNextImage);
        modal.addEventListener('click', function(e) {{
            if (e.target === modal) {{ closeModal(); }}
        }});
        document.addEventListener('keydown', function(e) {{
            if (modal.style.display === 'block') {{
                switch(e.key) {{
                    case 'Escape': closeModal(); break;
                    case 'ArrowLeft': showPrevImage(); break;
                    case 'ArrowRight': showNextImage(); break;
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
            photoItem.addEventListener('click', function() {{ openModal(index); }});
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
            const viewportHeight = window.innerHeight;
            const photoItems = document.querySelectorAll('.photo-item');
            photoItems.forEach((item, index) => {{
                const rect = item.getBoundingClientRect();
                const isVisible = rect.top < viewportHeight + 200 && rect.bottom > -200;
                if (!isVisible && loadedImages.has(index)) {{
                    const img = item.querySelector('img');
                    img.src = '';
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
        document.addEventListener('DOMContentLoaded', function() {{
            const photoGrid = document.getElementById('photo-grid');
            photos.forEach((photo, index) => {{
                const photoElement = createPhotoElement(photo, index);
                photoGrid.appendChild(photoElement);
            }});
            loadNextBatch();
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
            document.querySelectorAll('.photo-item').forEach(item => {{ observer.observe(item); }});
            let scrollTimeout;
            window.addEventListener('scroll', () => {{
                clearTimeout(scrollTimeout);
                scrollTimeout = setTimeout(unloadDistantImages, 1000);
            }});
            setInterval(() => {{
                if (currentBatch * batchSize < photos.length) {{ loadNextBatch(); }}
            }}, 2000);
        }});
    </script>
</body>
</html>
'''
    return html_content

def main():
    pictures_dir = Path('pictures')
    gallery_dir = Path('photo-gallery')
    gallery_dir.mkdir(exist_ok=True)
    # Get all subfolders in pictures/
    for folder in pictures_dir.iterdir():
        if not folder.is_dir():
            continue
        gallery_file = gallery_dir / f"{folder.name.lower().replace(' ', '-').replace('_', '-')}.html"
        if gallery_file.exists():
            print(f"Skipping {gallery_file} (already exists)")
            continue
        photos = get_photo_files(str(folder))
        if not photos:
            print(f"No photos found in {folder}")
            continue
        html = create_gallery_html(folder.name, photos)
        with open(gallery_file, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"Generated {gallery_file}")

if __name__ == "__main__":
    main() 