#!/usr/bin/env python3
"""
Image Optimizer for Slidev Presentations

Optimizes images for web presentation use:
- Resizes large images to appropriate dimensions
- Compresses for faster loading
- Converts formats if needed
- Generates responsive image variants

Usage:
    uv run python optimize_images.py [input_dir] [output_dir]
"""

import os
import sys
from pathlib import Path
from PIL import Image, ImageOps
import argparse


def optimize_image(input_path, output_path, max_width=1200, quality=85):
    """
    Optimize a single image for web presentation.

    Args:
        input_path: Path to input image
        output_path: Path for optimized output
        max_width: Maximum width in pixels
        quality: JPEG quality (1-100)
    """
    try:
        with Image.open(input_path) as img:
            # Convert to RGB if needed (for JPEG output)
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            # Calculate new dimensions maintaining aspect ratio
            width, height = img.size
            if width > max_width:
                ratio = max_width / width
                new_height = int(height * ratio)
                img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)

            # Auto-orient based on EXIF data
            img = ImageOps.exif_transpose(img)

            # Save optimized image
            output_path.parent.mkdir(parents=True, exist_ok=True)
            img.save(output_path, "JPEG", quality=quality, optimize=True)

            # Print optimization results
            original_size = os.path.getsize(input_path)
            new_size = os.path.getsize(output_path)
            compression_ratio = (1 - new_size / original_size) * 100

            print(f"✅ {input_path.name}")
            print(
                f"   {original_size // 1024}KB → {new_size // 1024}KB ({compression_ratio:.1f}% smaller)"
            )

    except Exception as e:
        print(f"❌ Error processing {input_path}: {e}")


def process_directory(input_dir, output_dir, max_width=1200, quality=85):
    """Process all images in a directory."""
    input_path = Path(input_dir)
    output_path = Path(output_dir)

    # Supported image extensions
    image_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp"}

    image_files = []
    for ext in image_extensions:
        image_files.extend(input_path.glob(f"**/*{ext}"))
        image_files.extend(input_path.glob(f"**/*{ext.upper()}"))

    if not image_files:
        print(f"No images found in {input_dir}")
        return

    print(f"🖼️  Processing {len(image_files)} images...")
    print(f"📂 Input: {input_dir}")
    print(f"📁 Output: {output_dir}")
    print(f"⚙️  Max width: {max_width}px, Quality: {quality}%")
    print()

    for img_file in image_files:
        # Maintain directory structure in output
        relative_path = img_file.relative_to(input_path)
        output_file = output_path / relative_path.with_suffix(".jpg")

        optimize_image(img_file, output_file, max_width, quality)


def create_responsive_variants(image_path, output_dir, sizes=[400, 800, 1200]):
    """Create responsive image variants for different screen sizes."""
    input_path = Path(image_path)
    output_path = Path(output_dir)

    print(f"🔄 Creating responsive variants for {input_path.name}...")

    with Image.open(input_path) as img:
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        for size in sizes:
            # Skip if image is already smaller than target size
            if img.width <= size:
                continue

            # Calculate new dimensions
            ratio = size / img.width
            new_height = int(img.height * ratio)
            resized = img.resize((size, new_height), Image.Resampling.LANCZOS)

            # Save with size suffix
            output_file = output_path / f"{input_path.stem}-{size}w.jpg"
            output_file.parent.mkdir(parents=True, exist_ok=True)
            resized.save(output_file, "JPEG", quality=85, optimize=True)

            file_size = os.path.getsize(output_file) // 1024
            print(f"   📱 {size}w: {file_size}KB")


def main():
    parser = argparse.ArgumentParser(
        description="Optimize images for Slidev presentations"
    )
    parser.add_argument(
        "input_dir",
        nargs="?",
        default="public/images",
        help="Input directory containing images (default: public/images)",
    )
    parser.add_argument(
        "output_dir",
        nargs="?",
        default="public/images/optimized",
        help="Output directory for optimized images (default: public/images/optimized)",
    )
    parser.add_argument(
        "--max-width",
        type=int,
        default=1200,
        help="Maximum image width in pixels (default: 1200)",
    )
    parser.add_argument(
        "--quality", type=int, default=85, help="JPEG quality 1-100 (default: 85)"
    )
    parser.add_argument(
        "--responsive",
        action="store_true",
        help="Create responsive variants (400w, 800w, 1200w)",
    )

    args = parser.parse_args()

    # Validate input directory
    if not os.path.exists(args.input_dir):
        print(f"❌ Input directory '{args.input_dir}' does not exist")
        print(f"💡 Create it and add your images, or specify a different path")
        sys.exit(1)

    if args.responsive:
        # Process each image individually for responsive variants
        import glob

        image_patterns = ["*.jpg", "*.jpeg", "*.png", "*.bmp", "*.tiff", "*.webp"]
        for pattern in image_patterns:
            for img_file in glob.glob(os.path.join(args.input_dir, pattern)):
                create_responsive_variants(img_file, args.output_dir)
    else:
        # Standard batch optimization
        process_directory(args.input_dir, args.output_dir, args.max_width, args.quality)

    print()
    print("✅ Image optimization complete!")
    print(f"💡 Use optimized images in your slides:")
    print(f"   ![Image](/{os.path.relpath(args.output_dir)}/your-image.jpg)")


if __name__ == "__main__":
    main()
