<?php
// Run daily via cron: 0 3 * * * php /path/to/cleanup.php
$temp_dir = __DIR__ . '/temp';
$max_age = 86400; // 24 hours

if (!is_dir($temp_dir)) {
    exit("Temp directory not found\n");
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

echo "Cleanup completed at " . date('Y-m-d H:i:s') . "\n";
