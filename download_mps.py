import requests
from bs4 import BeautifulSoup
import os
import time
from concurrent.futures import ThreadPoolExecutor

BASE_URL = "https://www.cdep.ro/pls/parlam/structura.mp?idm={id}&cam=2&leg=2024"
IMAGE_DIR = "mp_images"

if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

def download_image(mp_id):
    url = BASE_URL.format(id=mp_id)
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            print(f"Failed to fetch page for ID {mp_id}")
            return
        
        soup = BeautifulSoup(response.text, 'html.parser')
        # The image is usually in the first img tag with a specific path
        img_tag = soup.find('img', src=lambda s: s and '/parlamentari/l2024/' in s)
        
        if not img_tag:
            # Fallback search
            img_tag = soup.find('img', src=lambda s: s and '.JPG' in s.upper())
            
        if img_tag:
            img_url = img_tag['src']
            if img_url.startswith('/'):
                img_url = "https://www.cdep.ro" + img_url
            
            img_name = f"{mp_id}_{os.path.basename(img_url)}"
            img_path = os.path.join(IMAGE_DIR, img_name)
            
            img_response = requests.get(img_url, timeout=10)
            if img_response.status_code == 200:
                with open(img_path, 'wb') as f:
                    f.write(img_response.content)
                print(f"Downloaded {img_name}")
            else:
                print(f"Failed to download image for ID {mp_id}: {img_url}")
        else:
            print(f"No image found for ID {mp_id}")
            
    except Exception as e:
        print(f"Error processing ID {mp_id}: {e}")

def main():
    print("Starting download...")
    # Using ThreadPoolExecutor for faster downloads
    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(download_image, range(1, 332))
    print("Download finished.")

if __name__ == "__main__":
    main()
