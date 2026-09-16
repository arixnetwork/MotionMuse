<?php
// Run daily via cron: 0 3 * * * php /path/to/cleanup.php
$temp_dir = 'temp';
$max_age = 86400; // 24 hours

foreach (glob("$temp_dir/*") as $folder) {
    if (is_dir($folder) && (time() - filemtime($folder) > $max_age)) {
        array_map('unlink', glob("$folder/*.*"));
        rmdir($folder);
    }
}
echo "Cleanup completed at " . date('Y-m-d H:i:s');