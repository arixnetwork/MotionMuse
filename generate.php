<?php
header('Content-Type: application/json');

// Ensure system PATH includes common directories for ffmpeg and python
putenv("PATH=" . getenv("PATH") . ":/usr/local/bin:/usr/bin:/bin");

// Helper function to locate FFmpeg executable
function get_ffmpeg_binary() {
    // Check system ffmpeg first
    $system_ffmpeg = trim((string)shell_exec("which ffmpeg 2>/dev/null"));
    if (!empty($system_ffmpeg) && is_executable($system_ffmpeg)) {
        return $system_ffmpeg;
    }

    // Check python imageio_ffmpeg module binary
    $imageio_ffmpeg = trim((string)shell_exec("python3 -c 'import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())' 2>/dev/null"));
    if (!empty($imageio_ffmpeg) && is_executable($imageio_ffmpeg)) {
        return $imageio_ffmpeg;
    }

    // Fallback to plain command
    return "ffmpeg";
}

// Process animation request
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $prompt = $_POST['prompt'] ?? '';
    $duration = (int)($_POST['duration'] ?? 0);
    $style = $_POST['style'] ?? '';
    
    // Validate inputs
    if (empty($prompt) || $duration < 1 || $duration > 15) {
        echo json_encode([
            'success' => false,
            'error' => 'Invalid input parameters'
        ]);
        exit;
    }
    
    // Generate unique ID
    $session_id = uniqid('anim_');
    $output_dir = "temp/$session_id";
    
    // Create output directory
    if (!is_dir($output_dir)) {
        mkdir($output_dir, 0777, true);
    }
    
    // Execute Python AI script
    $command = "python3 ai-scripts/text2pose.py " .
        escapeshellarg("--prompt") . " " . escapeshellarg($prompt) . " " .
        escapeshellarg("--duration") . " " . escapeshellarg($duration) . " " .
        escapeshellarg("--style") . " " . escapeshellarg($style) . " " .
        escapeshellarg("--output") . " " . escapeshellarg($output_dir);
    
    $output = shell_exec("$command 2>&1");
    
    // Check if frames were generated
    $frameCount = count(glob("$output_dir/frame_*.png"));
    
    if ($frameCount > 0) {
        $ffmpeg_bin = get_ffmpeg_binary();
        // Convert to video
        $ffmpeg_cmd = escapeshellcmd($ffmpeg_bin) . " -y -framerate 24 -i " .
            escapeshellarg("$output_dir/frame_%04d.png") . " " .
            "-c:v libx264 -pix_fmt yuv420p -vf " . escapeshellarg("scale=trunc(iw/2)*2:trunc(ih/2)*2") . " " .
            escapeshellarg("$output_dir/output.mp4");
        
        $ffmpeg_output = shell_exec("$ffmpeg_cmd 2>&1");
        
        if (file_exists("$output_dir/output.mp4") && filesize("$output_dir/output.mp4") > 0) {
            // Return result
            echo json_encode([
                'success' => true,
                'download_url' => "$output_dir/output.mp4",
                'frame_count' => $frameCount
            ]);
        } else {
            echo json_encode([
                'success' => false,
                'error' => "Video rendering failed. Output: $ffmpeg_output"
            ]);
        }
    } else {
        // Cleanup empty directory
        if (is_dir($output_dir)) {
            rmdir($output_dir);
        }
        
        echo json_encode([
            'success' => false,
            'error' => "Animation generation failed. Output: $output"
        ]);
    }
} else {
    echo json_encode([
        'success' => false,
        'error' => 'Invalid request method'
    ]);
}
?>