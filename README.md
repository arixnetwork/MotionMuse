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
└── temp/ (auto-created)
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
