import argparse
import os
from PIL import Image
from tqdm import tqdm
import concurrent.futures

def process_image(img_path, output_dir, width, height, format):
    """
    Resizes and saves a single image.
    This function is designed to be run in a separate thread.
    """
    try:
        # 1. Open Image
        with Image.open(img_path) as img:
            
            # 2. Resize Logic
            # If width and height are None, we just convert format
            if width and height:
                # Image.Resampling.LANCZOS is high quality
                img = img.resize((width, height), Image.Resampling.LANCZOS)
            elif width:
                # Calculate height to maintain aspect ratio
                ratio = width / img.width
                new_height = int(img.height * ratio)
                img = img.resize((width, new_height), Image.Resampling.LANCZOS)

            # 3. Prepare Output Path
            filename = os.path.basename(img_path)
            name, _ = os.path.splitext(filename)
            
            # Handle format extension
            if format:
                ext = f".{format.lower()}"
                out_name = name + ext
            else:
                ext = os.path.splitext(filename)[1]
                out_name = filename
            
            out_path = os.path.join(output_dir, out_name)

            # 4. Save
            # Handle format specific saving (e.g., JPG doesn't support alpha/transparency)
            if format and format.upper() == 'JPEG' or format.upper() == 'JPG':
                # Convert RGBA to RGB to avoid errors
                if img.mode == 'RGBA':
                    img = img.convert('RGB')
            
            img.save(out_path)
            return f"Success: {filename}"
            
    except Exception as e:
        return f"Error processing {img_path}: {e}"

def main():
    parser = argparse.ArgumentParser(description="Bulk Image Resizer & Converter")
    parser.add_argument("input_dir", help="Folder containing images")
    parser.add_argument("output_dir", help="Folder to save processed images")
    parser.add_argument("-w", "--width", type=int, help="Target width in pixels")
    parser.add_argument("-H", "--height", type=int, help="Target height in pixels")
    parser.add_argument("-f", "--format", type=str, help="Output format (e.g., JPG, PNG, WEBP)")
    parser.add_argument("-s", "--scale", type=float, help="Scale factor (e.g., 0.5 for 50%%)")
    
    args = parser.parse_args()

    # Validation
    if not args.width and not args.height and not args.scale and not args.format:
        print("Error: Please provide at least one action (width, height, scale, or format).")
        return

    # Create output directory if it doesn't exist
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    # Get list of images
    valid_exts = ('.jpg', '.jpeg', '.png', '.webp', '.bmp', '.tiff')
    files = [os.path.join(args.input_dir, f) for f in os.listdir(args.input_dir) 
             if f.lower().endswith(valid_exts)]
    
    if not files:
        print("No images found in input directory.")
        return

    print(f"Processing {len(files)} images...")

    # --- MULTITHREADING LOGIC ---
    # We use ThreadPoolExecutor to process multiple images at once
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Map the process_image function to the list of files
        # We use tqdm to create a progress bar around the executor
        futures = []
        
        for img_path in files:
            # Handle Scale argument
            w, h = args.width, args.height
            if args.scale:
                with Image.open(img_path) as img:
                    w = int(img.width * args.scale)
                    h = int(img.height * args.scale)

            # Submit task to thread
            future = executor.submit(process_image, img_path, args.output_dir, w, h, args.format)
            futures.append(future)

        # Progress Bar wrapping
        for future in tqdm(concurrent.futures.as_completed(futures), total=len(files), colour="green"):
            result = future.result()
            # Optional: Print errors if needed
            if "Error" in result:
                print(result)

    print(f"\nDone! Images saved to: {args.output_dir}")

if __name__ == "__main__":
    main()