import subprocess
import re
import os
from concurrent.futures import ThreadPoolExecutor

BASE_URL = "https://www.cdep.ro/pls/parlam/structura.mp?idm={id}&cam=2&leg=2024"
IMAGE_DIR = "mp_images"

if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

def get_image_url(mp_id):
    url = BASE_URL.format(id=mp_id)
    try:
        # Use curl to get the page content
        result = subprocess.run(['curl', '-s', url], capture_output=True, text=True, encoding='latin-1')
        if result.returncode != 0:
            return None
        
        # Search for the image pattern
        match = re.search(r'img src="(/parlamentari/l2024/.*?\.JPG)"', result.stdout, re.IGNORECASE)
        if match:
            return "https://www.cdep.ro" + match.group(1)
        
        # Try a different pattern
        match = re.search(r'img src="(/img/parlam/2024/.*?\.jpg)"', result.stdout, re.IGNORECASE)
        if match:
            return "https://www.cdep.ro" + match.group(1)
            
    except Exception as e:
        print(f"Error getting URL for ID {mp_id}: {e}")
    return None

def download_image(mp_id):
    img_url = get_image_url(mp_id)
    if not img_url:
        print(f"No image found for ID {mp_id}")
        return
    
    img_name = f"{mp_id}_{os.path.basename(img_url)}"
    img_path = os.path.join(IMAGE_DIR, img_name)
    
    try:
        # Use curl to download the image
        subprocess.run(['curl', '-s', '-o', img_path, img_url])
        if os.path.exists(img_path) and os.path.getsize(img_path) > 0:
            print(f"Downloaded {img_name}")
        else:
            print(f"Failed to download image for ID {mp_id}: {img_url}")
    except Exception as e:
        print(f"Error downloading for ID {mp_id}: {e}")

def main():
    print("Starting download with curl...")
    with ThreadPoolExecutor(max_workers=15) as executor:
        executor.map(download_image, range(1, 332))
    print("Download finished.")

if __name__ == "__main__":
    main()
