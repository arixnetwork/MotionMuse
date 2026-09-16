<?php
header('Content-Type: application/json');

// Process animation request
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $prompt = $_POST['prompt'];
    $duration = (int)$_POST['duration'];
    $style = $_POST['style'];
    
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
        // Convert to video
        $ffmpeg_cmd = "ffmpeg -y -framerate 24 -i " . 
            escapeshellarg("$output_dir/frame_%04d.png") . " " .
            "-c:v libx264 -pix_fmt yuv420p -vf 'scale=trunc(iw/2)*2:trunc(ih/2)*2' " .
            escapeshellarg("$output_dir/output.mp4");
        
        shell_exec($ffmpeg_cmd);
        
        // Return result
        echo json_encode([
            'success' => true,
            'download_url' => "$output_dir/output.mp4",
            'frame_count' => $frameCount
        ]);
    } else {
        // Cleanup empty directory
        rmdir($output_dir);
        
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