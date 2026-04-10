import os
from PIL import Image
from transformers import pipeline
import torch
import json
from tqdm import tqdm

MODEL_NAME = "openai/clip-vit-base-patch32"
IMAGE_DIR = "mp_images"
LABELS = ["a person with a beard", "a person without a beard"]

def main():
    print("Loading model...")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    classifier = pipeline("zero-shot-image-classification", model=MODEL_NAME, device=device)
    
    images = [f for f in os.listdir(IMAGE_DIR) if f.lower().endswith((".jpg", ".jpeg"))]
    print(f"Total images found: {len(images)}")
    
    results_list = []
    stats = {
        "with_beard": 0,
        "without_beard": 0,
        "errors": 0
    }
    
    print("Starting full analysis...")
    # Use tqdm if available, otherwise just print every 10
    for i, img_name in enumerate(tqdm(images, desc="Analyzing")):
        img_path = os.path.join(IMAGE_DIR, img_name)
        try:
            with Image.open(img_path) as img:
                # Convert to RGB to ensure compatibility
                img = img.convert("RGB")
                results = classifier(img, candidate_labels=LABELS)
                
            top_result = results[0]
            label = top_result['label']
            score = top_result['score']
            
            results_list.append({
                "image": img_name,
                "label": label,
                "confidence": score
            })
            
            if label == LABELS[0]:
                stats["with_beard"] += 1
            else:
                stats["without_beard"] += 1
                
        except Exception as e:
            print(f"Error analyzing {img_name}: {e}")
            stats["errors"] += 1
            
    # Save results to JSON
    with open("beard_stats.json", "w") as f:
        json.dump({"stats": stats, "details": results_list}, f, indent=4)
    
    print("\n--- Statistics ---")
    print(f"Total analyzed: {len(images)}")
    print(f"People with beards: {stats['with_beard']}")
    print(f"People without beards: {stats['without_beard']}")
    print(f"Errors: {stats['errors']}")
    
    if len(images) > 0:
        percent = (stats['with_beard'] / (stats['with_beard'] + stats['without_beard'])) * 100
        print(f"Percentage with beards: {percent:.2f}%")

if __name__ == "__main__":
    main()
