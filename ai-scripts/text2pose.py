#!/usr/bin/env python3
"""
MotionMuse AI Animation Generator
Version: 1.1.0
Requirements: pillow, numpy
"""

import argparse
import os
import sys
import random
import time
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# Font setup (use default system font if arial is unavailable)
try:
    font = ImageFont.truetype("arial.ttf", 24)
except Exception:
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
    elif style == "claymation":
        add_claymation_elements(draw, width, height, frame_num)
    elif style == "lowpoly":
        add_lowpoly_elements(draw, width, height, frame_num)
    elif style == "noir":
        add_noir_elements(draw, width, height, frame_num)
    elif style == "synthwave":
        add_synthwave_elements(draw, width, height, frame_num)
    elif style == "sketch":
        add_sketch_elements(draw, width, height, frame_num)
    elif style == "fantasy":
        add_fantasy_elements(draw, width, height, frame_num)
    elif style == "steampunk":
        add_steampunk_elements(draw, width, height, frame_num)
    elif style == "vector":
        add_vector_elements(draw, width, height, frame_num)
    else:
        # Fallback default
        add_cyberpunk_elements(draw, width, height, frame_num)
    
    return img

def get_bg_color(style, progress):
    colors = {
        "cyberpunk": (20, 10, 40),
        "watercolor": (240, 248, 255),
        "pixel": (0, 0, 0),
        "anime": (255, 250, 240),
        "retro": (0, 0, 70),
        "claymation": (180, 140, 100),
        "lowpoly": (30, 40, 60),
        "noir": (15, 15, 15),
        "synthwave": (25, 0, 50),
        "sketch": (245, 245, 240),
        "fantasy": (40, 20, 60),
        "steampunk": (50, 30, 15),
        "vector": (250, 250, 250)
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
        "retro": (255, 223, 0),
        "claymation": (255, 255, 240),
        "lowpoly": (100, 220, 255),
        "noir": (240, 240, 240),
        "synthwave": (255, 105, 180),
        "sketch": (30, 30, 30),
        "fantasy": (255, 215, 0),
        "steampunk": (218, 165, 32),
        "vector": (40, 40, 40)
    }.get(style, (255, 255, 255))

def get_progress_color(style):
    return {
        "cyberpunk": (255, 0, 255),
        "watercolor": (100, 149, 237),
        "pixel": (0, 255, 0),
        "anime": (255, 105, 180),
        "retro": (255, 0, 0),
        "claymation": (210, 105, 30),
        "lowpoly": (0, 206, 209),
        "noir": (200, 200, 200),
        "synthwave": (0, 255, 255),
        "sketch": (80, 80, 80),
        "fantasy": (147, 112, 219),
        "steampunk": (184, 115, 51),
        "vector": (255, 69, 0)
    }.get(style, (0, 150, 255))

# Style-specific drawing functions
def add_cyberpunk_elements(draw, width, height, frame_num):
    for i in range(0, width, 20):
        draw.line([(i, 0), (i, height)], fill=(0, 255, 255), width=1)
    size = 50 + 20 * np.sin(frame_num/10)
    x = width/2 + 100 * np.sin(frame_num/15)
    y = height/2 + 80 * np.cos(frame_num/12)
    draw.ellipse([x-size, y-size, x+size, y+size], outline=(255, 0, 255), width=3)

def add_watercolor_elements(draw, width, height, frame_num):
    for _ in range(5):
        x = random.randint(0, width)
        y = height/2 + 100 * np.sin(frame_num/20 + x/100)
        size = 30 + 20 * abs(np.sin(frame_num/15))
        color = (
            random.randint(100, 200),
            random.randint(100, 200),
            random.randint(150, 230)
        )
        draw.ellipse([x-size, y-size, x+size, y+size], fill=color)

def add_pixel_elements(draw, width, height, frame_num):
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

def add_anime_elements(draw, width, height, frame_num):
    center_x, center_y = width // 2, height // 2
    for angle in range(0, 360, 15):
        rad = np.radians(angle + frame_num * 2)
        r_inner = 50 + 10 * np.sin(frame_num / 5)
        r_outer = 300
        x1 = center_x + r_inner * np.cos(rad)
        y1 = center_y + r_inner * np.sin(rad)
        x2 = center_x + r_outer * np.cos(rad)
        y2 = center_y + r_outer * np.sin(rad)
        draw.line([(x1, y1), (x2, y2)], fill=(255, 200, 220), width=2)
    x = center_x + 120 * np.cos(frame_num / 10)
    y = center_y + 60 * np.sin(frame_num / 8)
    draw.polygon([
        (x, y - 15), (x + 5, y - 5), (x + 15, y), (x + 5, y + 5),
        (x, y + 15), (x - 5, y + 5), (x - 15, y), (x - 5, y - 5)
    ], fill=(255, 255, 100))

def add_retro_elements(draw, width, height, frame_num):
    sun_x, sun_y = width // 2, height // 2 - 20
    draw.ellipse([sun_x - 60, sun_y - 60, sun_x + 60, sun_y + 60], fill=(255, 128, 0))
    for y in range(height // 2, height, 15):
        offset_y = y + (frame_num % 15)
        if offset_y < height:
            draw.line([(0, offset_y), (width, offset_y)], fill=(255, 0, 128), width=2)

def add_claymation_elements(draw, width, height, frame_num):
    cx, cy = width // 2, height // 2
    r = 60 + 10 * np.sin(frame_num / 6)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(220, 100, 80), outline=(150, 60, 40), width=4)
    draw.ellipse([cx - r//2, cy - r//2, cx + r//3, cy + r//3], fill=(240, 140, 120))

def add_lowpoly_elements(draw, width, height, frame_num):
    cx, cy = width // 2, height // 2
    pts = [
        (cx + 80 * np.cos(frame_num/10), cy + 80 * np.sin(frame_num/10)),
        (cx + 120 * np.cos(frame_num/10 + 2), cy + 60 * np.sin(frame_num/10 + 2)),
        (cx + 40 * np.cos(frame_num/10 + 4), cy + 100 * np.sin(frame_num/10 + 4))
    ]
    draw.polygon(pts, fill=(0, 180, 220), outline=(255, 255, 255), width=2)

def add_noir_elements(draw, width, height, frame_num):
    for i in range(0, width, 40):
        draw.line([(i + (frame_num*3)%40, 0), (i + (frame_num*3)%40 - 100, height)], fill=(80, 80, 80), width=3)
    cx, cy = width // 2, height // 2
    draw.rectangle([cx - 40, cy - 60, cx + 40, cy + 60], fill=(255, 255, 255), outline=(0, 0, 0), width=3)

def add_synthwave_elements(draw, width, height, frame_num):
    cx, cy = width // 2, height // 2 - 30
    draw.ellipse([cx - 80, cy - 80, cx + 80, cy + 80], fill=(255, 0, 128))
    for y in range(cy + 10, height, 12):
        draw.line([(0, y), (width, y)], fill=(0, 255, 255), width=2)

def add_sketch_elements(draw, width, height, frame_num):
    cx, cy = width // 2, height // 2
    for _ in range(12):
        ox = random.randint(-5, 5)
        oy = random.randint(-5, 5)
        draw.ellipse([cx - 50 + ox, cy - 50 + oy, cx + 50 + ox, cy + 50 + oy], outline=(50, 50, 50), width=1)

def add_fantasy_elements(draw, width, height, frame_num):
    cx, cy = width // 2, height // 2
    for i in range(8):
        angle = frame_num / 8 + i * np.pi / 4
        x = cx + 90 * np.cos(angle)
        y = cy + 50 * np.sin(angle)
        draw.ellipse([x - 15, y - 15, x + 15, y + 15], fill=(218, 112, 214), outline=(255, 215, 0), width=2)

def add_steampunk_elements(draw, width, height, frame_num):
    cx, cy = width // 2, height // 2
    # Gear
    r = 50
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(184, 115, 51), outline=(120, 70, 20), width=3)
    for a in range(0, 360, 45):
        rad = np.radians(a + frame_num * 3)
        gx = cx + (r + 10) * np.cos(rad)
        gy = cy + (r + 10) * np.sin(rad)
        draw.rectangle([gx - 5, gy - 5, gx + 5, gy + 5], fill=(218, 165, 32))

def add_vector_elements(draw, width, height, frame_num):
    cx, cy = width // 2, height // 2
    x = cx + 80 * np.cos(frame_num / 12)
    draw.rectangle([x - 40, cy - 40, x + 40, cy + 40], fill=(255, 87, 34))

if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("--prompt", type=str, required=True)
        parser.add_argument("--duration", type=int, default=5)
        parser.add_argument("--style", type=str, default="cyberpunk")
        parser.add_argument("--output", type=str, required=True)
        args = parser.parse_args()

        start_time = time.time()
        generate_animation(args.prompt, args.duration, args.style, args.output)
        print(f"Completed in {time.time() - start_time:.2f} seconds")
    except Exception as e:
        print(f"ERROR: {str(e)}")
        sys.exit(1)
