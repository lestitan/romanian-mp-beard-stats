import subprocess
import re
import os
import json
from concurrent.futures import ThreadPoolExecutor

BASE_URL = "https://www.cdep.ro/pls/parlam/structura.mp?idm={id}&cam=2&leg=2024"

def get_mp_name(mp_id):
    url = BASE_URL.format(id=mp_id)
    try:
        # Use curl to get the page content with correct encoding
        result = subprocess.run(['curl', '-s', url], capture_output=True, text=True, encoding='latin-1')
        if result.returncode != 0:
            return None
        
        # Look for the name in the alt attribute of the image or in the text following it
        # The user provided a snippet: alt="Dragoş Gabriel Zisopol"
        match = re.search(r'alt="([^"]+)"', result.stdout)
        if match:
            return match.group(1).strip()
            
    except Exception as e:
        print(f"Error getting name for ID {mp_id}: {e}")
    return f"MP ID {mp_id}"

def main():
    print("Mapping IDs to names...")
    mp_names = {}
    
    # Using a smaller pool to avoid overwhelming the server
    with ThreadPoolExecutor(max_workers=10) as executor:
        ids = range(1, 332)
        results = list(executor.map(get_mp_name, ids))
        
        for mp_id, name in zip(ids, results):
            if name:
                mp_names[str(mp_id)] = name
    
    with open('mp_names.json', 'w', encoding='utf-8') as f:
        json.dump(mp_names, f, indent=4, ensure_ascii=False)
    print("Mapping finished: mp_names.json")

if __name__ == "__main__":
    main()
