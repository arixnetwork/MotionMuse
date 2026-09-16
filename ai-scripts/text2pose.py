import argparse
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import random
import time

# Font setup (use default system font)
try:
    font = ImageFont.truetype("arial.ttf", 24)
except:
    font = ImageFont.load_default()

def generate_animation(prompt, duration, style, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    frames = duration * 24  # 24fps
    
    print(f"Generating {frames} frames for: '{prompt}' in {style} style")
    
    # Generate frames
    for i in range(frames):
        progress = i / frames
        img = create_frame(prompt, style, progress, i)
        img.save(os.path.join(output_dir, f"frame_{i:04d}.png"))
        print(f"Generated frame {i+1}/{frames}")

def create_frame(prompt, style, progress, frame_num):
    width, height = 640, 360
    img = Image.new('RGB', (width, height), color=get_bg_color(style, progress))
    draw = ImageDraw.Draw(img)
    
    # Add prompt text
    draw.text((10, 10), f'"{prompt}"', fill=get_text_color(style), font=font)
    
    # Add style indicator
    draw.text((10, height-30), f'Style: {style}', fill=get_text_color(style), font=font)
    
    # Add progress indicator
    bar_width = width - 20
    draw.rectangle([10, height-60, 10 + bar_width, height-50], fill=(200, 200, 200))
    draw.rectangle([10, height-60, 10 + int(bar_width * progress), height-50], fill=get_progress_color(style))
    
    # Add animated elements based on style
    if style == "cyberpunk":
        add_cyberpunk_elements(draw, width, height, frame_num)
    elif style == "watercolor":
        add_watercolor_elements(draw, width, height, frame_num)
    elif style == "pixel":
        add_pixel_elements(draw, width, height, frame_num)
    elif style == "anime":
        add_anime_elements(draw, width, height, frame_num)
    elif style == "retro":
        add_retro_elements(draw, width, height, frame_num)
    
    return img

def get_bg_color(style, progress):
    colors = {
        "cyberpunk": (20, 10, 40),
        "watercolor": (240, 248, 255),
        "pixel": (0, 0, 0),
        "anime": (255, 250, 240),
        "retro": (0, 0, 70)
    }
    base = colors.get(style, (70, 130, 180))
    
    # Add subtle animation to background
    pulse = int(128 * abs((progress * 2) % 2 - 1))
    return (
        max(0, min(255, base[0] + pulse)),
        max(0, min(255, base[1] + pulse)),
        max(0, min(255, base[2] + pulse))
    )

def get_text_color(style):
    return {
        "cyberpunk": (0, 255, 255),
        "watercolor": (70, 70, 70),
        "pixel": (0, 255, 0),
        "anime": (50, 50, 150),
        "retro": (255, 223, 0)
    }.get(style, (255, 255, 255))

def get_progress_color(style):
    return {
        "cyberpunk": (255, 0, 255),
        "watercolor": (100, 149, 237),
        "pixel": (0, 255, 0),
        "anime": (255, 105, 180),
        "retro": (255, 0, 0)
    }.get(style, (0, 150, 255))

# Style-specific drawing functions
def add_cyberpunk_elements(draw, width, height, frame_num):
    # Grid lines
    for i in range(0, width, 20):
        alpha = int(100 + 100 * abs((frame_num/10 + i/50) % 2 - 1))
        draw.line([(i, 0), (i, height)], fill=(0, 255, 255, alpha), width=1)
    
    # Moving neon shapes
    size = 50 + 20 * np.sin(frame_num/10)
    x = width/2 + 100 * np.sin(frame_num/15)
    y = height/2 + 80 * np.cos(frame_num/12)
    draw.ellipse([x-size, y-size, x+size, y+size], outline=(255, 0, 255), width=3)

def add_watercolor_elements(draw, width, height, frame_num):
    # Blob shapes
    for _ in range(5):
        x = random.randint(0, width)
        y = height/2 + 100 * np.sin(frame_num/20 + x/100)
        size = 30 + 20 * abs(np.sin(frame_num/15))
        color = (
            random.randint(100, 200),
            random.randint(100, 200),
            random.randint(150, 230),
            180
        )
        draw.ellipse([x-size, y-size, x+size, y+size], fill=color)

def add_pixel_elements(draw, width, height, frame_num):
    # Pixel grid
    pixel_size = 10
    for x in range(0, width, pixel_size):
        for y in range(0, height, pixel_size):
            if (x//pixel_size + y//pixel_size + frame_num) % 4 == 0:
                draw.rectangle(
                    [x, y, x+pixel_size-1, y+pixel_size-1],
                    fill=(
                        int(255 * abs(np.sin(frame_num/10 + x/100))),
                        int(255 * abs(np.cos(frame_num/8 + y/100))),
                        int(255 * abs(np.sin(frame_num/12 + (x+y)/100)))
                    )
                )

# ... (similar functions for anime and retro styles)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", type=str, required=True)
    parser.add_argument("--duration", type=int, default=5)
    parser.add_argument("--style", type=str, default="cyberpunk")
    parser.add_argument("--output", type=str, required=True)
    args = parser.parse_args()
    
    start_time = time.time()
    generate_animation(args.prompt, args.duration, args.style, args.output)
    print(f"Completed in {time.time() - start_time:.2f} seconds")