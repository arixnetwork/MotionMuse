# MotionMuse - Deployment & Release Guide (v1.1.0)

MotionMuse is a lightweight, web-based AI animation generator designed for cPanel and Linux web hosting environments.

## Release v1.1.0 Highlights
- **Supported MotionMuse Models / Styles**:
  - Cyberpunk
  - Watercolor
  - Pixel Art
  - Anime
  - Retro 80s
  - 3D Claymation
  - Low Poly 3D
  - Film Noir
  - Synthwave
  - Pencil Sketch
  - Fantasy / Dreamscape
  - Steampunk
  - Minimalist Vector
- **Security & Performance**: Enhanced `.htaccess` rules with Content Security Policy headers and mod_deflate output compression.
- **Improved Maintenance**: Robust temporary directory cleanup (`cleanup.php`) via automated daily cron tasks.

## System Requirements
- cPanel/Linux hosting with SSH access
- PHP 8.0+
- Python 3.9+
- FFmpeg (or Python `imageio-ffmpeg` package)
- MySQL/MariaDB (optional)

## File Structure
```
public_html/
├── index.php
├── generate.php
├── cleanup.php
├── .htaccess
├── ai-scripts/
│   └── text2pose.py
├── models/
│   └── motionmuse/ (claymation, low_poly, film_noir, synthwave, sketch, fantasy, steampunk, vector, cyberpunk, watercolor, pixel_art, anime, retro_80s)
└── temp/ (auto-created)
```

## Model Setup & Directory Pipeline

To clone and set up all 13 MotionMuse models onto your Linux environment, follow these terminal instructions:

### 1. Create the Directory Structure
Run this `mkdir` command in your project root to generate the target folders for all 13 styles:
```bash
mkdir -p models/motionmuse/{claymation,low_poly,film_noir,synthwave,sketch,fantasy,steampunk,vector,cyberpunk,watercolor,pixel_art,anime,retro_80s}
```

### 2. Install Git LFS (If cloning from Hugging Face / Git)
Large model files (`.safetensors`, `.ckpt`, `.bin`) require Git Large File Storage. Install it via your Linux package manager:

- **Ubuntu / Debian**:
  ```bash
  sudo apt update && sudo apt install git-lfs -y
  git lfs install
  ```

- **CentOS / RHEL / Fedora**:
  ```bash
  sudo dnf install git-lfs -y
  git lfs install
  ```

### 3. Bulk Download via Linux Terminal
If the models are hosted on a web server or cloud storage bucket, use `wget` or `curl` to loop through them automatically:
```bash
# Define the array of styles
MODELS=("claymation" "low_poly" "film_noir" "synthwave" "sketch" "fantasy" "steampunk" "vector" "cyberpunk" "watercolor" "pixel_art" "anime" "retro_80s")

# Base URL where your files are hosted
BASE_URL="https://your-model-source.com"

# Loop and download each one into its corresponding folder
for model in "${MODELS[@]}"; do
    echo "Downloading ${model}..."
    wget -P "models/motionmuse/${model}/" "${BASE_URL}/${model}.safetensors"
done
```

### 4. Adjust Permissions
Ensure your web server or Python execution environment has read access to model files:
```bash
chmod -R 755 models/motionmuse/
```

## Installation & Deployment

### 1. Upload Files
Upload all repository files to your domain's `public_html` directory using cPanel File Manager or FTP.

### 2. Create Directories
```bash
mkdir -p public_html/ai-scripts
mkdir -p public_html/temp
```

### 3. Set Permissions
```bash
chmod 755 public_html
chmod 644 public_html/index.php
chmod 644 public_html/generate.php
chmod 644 public_html/cleanup.php
chmod 644 public_html/.htaccess
chmod 755 public_html/ai-scripts
chmod 644 public_html/ai-scripts/text2pose.py
chmod 777 public_html/temp
```

### 4. Install Python Dependencies (via SSH)
```bash
pip3 install pillow numpy imageio imageio-ffmpeg
```

### 5. Verify FFmpeg Installation
```bash
ffmpeg -version
```

### 6. Configure Cron Job (Daily Cleanup)
In cPanel:
1. Navigate to **Advanced > Cron Jobs**
2. Add a new cron job:
   ```
   Command: /usr/local/bin/php /home/YOUR_CPANEL_USER/public_html/cleanup.php
   Schedule: Daily at 3:00 AM (0 3 * * *)
   ```

### 7. Test Installation
1. Visit `https://linkparty.info`
2. Enter an animation description (e.g. "Dancing Robot in Neon City")
3. Select a model/style (e.g. "Cyberpunk" or "3D Claymation")
4. Click "Generate Animation"
5. Download the MP4 file once rendering finishes.

---
**Support**: For questions or support, contact `support@linkparty.info`.
