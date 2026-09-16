# MotionMuse - Deployment Guide

This guide explains how to deploy the MotionMuse clone to your cPanel hosting environmen

## System Requirements
- cPanel/Linux hosting with SSH access
- PHP 8.0+
- Python 3.9+
- FFmpeg
- MySQL/MariaDB (optional)

### README.md - MotionMuse Clone Installation Guide

```markdown
# MotionMuse Clone - Deployment Guide

This guide explains how to deploy the MotionMuse clone to your cPanel hosting environment at `linkparty.info`.

## System Requirements
- cPanel/Linux hosting with SSH access
- PHP 8.0+
- Python 3.9+
- FFmpeg
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

## Installation Steps

### 1. Upload Files
Upload all files to your `public_html` directory using cPanel File Manager or FTP.

### 2. Create Directories
```bash
mkdir -p public_html/ai-scripts
mkdir public_html/temp
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
pip3 install pillow numpy
```

### 5. Verify FFmpeg Installation
```bash
ffmpeg -version
```
If not installed, contact your hosting provider or install manually:
```bash
sudo apt-get install ffmpeg -y
```

### 6. Configure Cron Job (Daily Cleanup)
In cPanel:
1. Go to **Advanced > Cron Jobs**
2. Add new job:
   ```
   Command: /usr/local/bin/php /home/YOUR_CPANEL_USER/public_html/cleanup.php
   Schedule: Daily at 3:00 AM
   ```

### 7. Test Installation
1. Visit `https://linkparty.info`
2. Enter a prompt (e.g., "dancing robot")
3. Click "Generate Animation"
4. Verify MP4 download appears after 10-30 seconds

## Configuration Options

### Enable Database (Optional)
Add this to `generate.php` for MySQL logging:
```php
// Add to top of generate.php
$db = new mysqli('localhost', 'DB_USER', 'DB_PASS', 'DB_NAME');

// After successful generation
$db->query("INSERT INTO animations (session_id, prompt, duration, style, created_at) 
            VALUES ('$session_id', '$prompt', $duration, '$style', NOW())");
```

### Increase Performance
Add to `.htaccess`:
```apache
<IfModule mod_expires.c>
    ExpiresActive On
    ExpiresByType image/png "access plus 1 year"
    ExpiresByType video/mp4 "access plus 1 month"
</IfModule>
```

## Troubleshooting

### Common Issues
1. **Blank page after submission**:
   - Check PHP error logs
   - Verify `temp/` directory has write permissions (777)
   
2. **FFmpeg not found**:
   ```php
   // Add to generate.php before ffmpeg command
   putenv("PATH=" . getenv("PATH") . ":/usr/local/bin:/usr/bin");
   ```

3. **Python script not running**:
   ```bash
   # Test manually
   python3 public_html/ai-scripts/text2pose.py --prompt "test" --duration 2 --style cyberpunk --output test_output
   ```

### Security Notes
- Change `.htaccess` rules to restrict access if needed
- Consider moving `ai-scripts` outside public_html
- Add Cloudflare firewall rules

## Next Steps for Enhancement
1. Integrate Stable Diffusion API
2. Add user accounts system
3. Implement payment processing
4. Add social sharing features

---
**Support**: For assistance, contact support@linkparty.info
```

### File: cleanup.php (Updated)
```php
<?php
// Run daily via cron: 0 3 * * * php /path/to/cleanup.php
$temp_dir = __DIR__ . '/temp';
$max_age = 86400; // 24 hours

if (!is_dir($temp_dir)) {
    exit("Temp directory not found");
}

foreach (scandir($temp_dir) as $item) {
    if ($item === '.' || $item === '..') continue;
    
    $path = $temp_dir . '/' . $item;
    if (is_dir($path) && (time() - filemtime($path) > $max_age)) {
        // Delete files in directory
        array_map('unlink', glob("$path/*.*"));
        // Delete directory
        rmdir($path);
        echo "Deleted: $path\n";
    }
}

echo "Cleanup completed at " . date('Y-m-d H:i:s');
```

### File: .htaccess (Updated Security)
```apache
# Security protections
<IfModule mod_headers.c>
    Header always set X-Content-Type-Options "nosniff"
    Header always set X-Frame-Options "SAMEORIGIN"
    Header always set Content-Security-Policy "default-src 'self'; script-src 'self' cdnjs.cloudflare.com; style-src 'self' cdn.jsdelivr.net; img-src 'self' data:; media-src 'self' data:;"
    Header always set Referrer-Policy "strict-origin"
</IfModule>

# Prevent directory listing
Options -Indexes

# Protect sensitive files
<FilesMatch "(\.py|\.log|\.env|generate\.php|cleanup\.php)$">
    Require all denied
</FilesMatch>

# Block access to temp directory
<Directory "temp">
    Require all denied
</Directory>

# Enable pretty URLs
RewriteEngine On
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^(.*)$ index.php [L,QSA]

# Compression
<IfModule mod_deflate.c>
    AddOutputFilterByType DEFLATE text/html text/css application/javascript
</IfModule>
```

### File: ai-scripts/text2pose.py (Updated Header)
```python
#!/usr/bin/env python3
"""
MotionMuse AI Animation Generator
Version: 1.2
Requirements: pillow, numpy
"""

import argparse
import os
import numpy as np
from PIL import Image, ImageDraw
import random
import time
import sys

# Add error handling
try:
    # ... [rest of the code] ...
    
except Exception as e:
    print(f"ERROR: {str(e)}")
    sys.exit(1)
```

This completes all files with installation instructions. The project is now ready for deployment to your cPanel hosting at linkparty.info!