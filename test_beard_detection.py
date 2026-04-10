import os
from PIL import Image
from transformers import pipeline
import torch

# Use a smaller CLIP model
MODEL_NAME = "openai/clip-vit-base-patch32"

def main():
    print("Loading model...")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    classifier = pipeline("zero-shot-image-classification", model=MODEL_NAME, device=device)
    
    image_dir = "mp_images"
    images = [f for f in os.listdir(image_dir) if f.endswith(".JPG") or f.endswith(".jpg")]
    
    # Test with first 10 images
    test_images = images[:10]
    labels = ["a person with a beard", "a person without a beard"]
    
    print(f"Analyzing {len(test_images)} images...")
    for img_name in test_images:
        img_path = os.path.join(image_dir, img_name)
        try:
            # Check if image is valid
            with Image.open(img_path) as img:
                img.verify()
            
            # Re-open for classification (verify closes the file)
            img = Image.open(img_path)
            
            results = classifier(img, candidate_labels=labels)
            
            # Print result
            top_result = results[0]
            print(f"{img_name}: {top_result['label']} (confidence: {top_result['score']:.2f})")
            
        except Exception as e:
            print(f"Error analyzing {img_name}: {e}")

if __name__ == "__main__":
    main()
