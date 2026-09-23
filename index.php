<?php
// DOMAIN: linkparty.info
header('Content-Type: text/html; charset=utf-8');
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MotionMuse Clone | linkparty.info</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        .gradient-bg {
            background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
            min-height: 100vh;
        }
        #previewCanvas { 
            border: 2px dashed #0d6efd; 
            background: #f8f9fa;
            max-width: 100%;
        }
        .card {
            border-radius: 15px;
            overflow: hidden;
        }
        .card-header {
            font-weight: 700;
            letter-spacing: 1px;
        }
    </style>
</head>
<body class="gradient-bg">
    <div class="container py-5">
        <div class="card shadow-lg">
            <div class="card-header bg-white d-flex justify-content-between align-items-center">
                <h1 class="h3 mb-0">🎬 MotionMuse Clone</h1>
                <span class="badge bg-primary">v1.1.0</span>
            </div>
            <div class="card-body">
                <form id="animationForm" action="generate.php" method="POST">
                    <div class="mb-3">
                        <label class="form-label">Describe your animation:</label>
                        <input type="text" name="prompt" class="form-control" 
                               placeholder="e.g. 'Jazz dancer in neon lights'" required>
                    </div>
                    
                    <div class="row mb-3">
                        <div class="col-md-6">
                            <label>Duration (seconds):</label>
                            <input type="number" name="duration" class="form-control" value="5" min="1" max="15">
                        </div>
                        <div class="col-md-6">
                            <label>Model / Style:</label>
                            <select name="style" class="form-select">
                                <option value="cyberpunk">Cyberpunk</option>
                                <option value="watercolor">Watercolor</option>
                                <option value="pixel">Pixel Art</option>
                                <option value="anime">Anime</option>
                                <option value="retro">Retro 80s</option>
                                <option value="claymation">3D Claymation</option>
                                <option value="lowpoly">Low Poly 3D</option>
                                <option value="noir">Film Noir</option>
                                <option value="synthwave">Synthwave</option>
                                <option value="sketch">Pencil Sketch</option>
                                <option value="fantasy">Fantasy / Dreamscape</option>
                                <option value="steampunk">Steampunk</option>
                                <option value="vector">Minimalist Vector</option>
                            </select>
                        </div>
                    </div>
                    
                    <button type="submit" class="btn btn-primary w-100 py-3">
                        Generate Animation
                    </button>
                </form>
                
                <div class="mt-4 text-center">
                    <canvas id="previewCanvas" width="640" height="360"></canvas>
                    <div id="resultContainer" class="mt-3"></div>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script>
        // Initialize Three.js preview
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(75, 640/360, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({
            canvas: document.getElementById('previewCanvas'),
            antialias: true
        });
        renderer.setClearColor(0xf8f9fa);
        
        // Add sample animation object
        const geometry = new THREE.TorusKnotGeometry(1, 0.3, 128, 16);
        const material = new THREE.MeshPhongMaterial({
            color: 0x0d6efd,
            shininess: 80
        });
        const knot = new THREE.Mesh(geometry, material);
        scene.add(knot);
        
        // Add lighting
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
        scene.add(ambientLight);
        
        const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
        directionalLight.position.set(10, 10, 10);
        scene.add(directionalLight);
        
        camera.position.z = 5;

        // Animation loop
        function animate() {
            requestAnimationFrame(animate);
            knot.rotation.x += 0.01;
            knot.rotation.y += 0.01;
            renderer.render(scene, camera);
        }
        animate();
        
        // Form submission handler
        document.getElementById('animationForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const form = e.target;
            const resultContainer = document.getElementById('resultContainer');
            resultContainer.innerHTML = '<div class="spinner-border text-primary" role="status"></div><p class="mt-2">Generating animation...</p>';
            
            try {
                const response = await fetch(form.action, {
                    method: 'POST',
                    body: new FormData(form)
                });
                
                const data = await response.json();
                if (data.success) {
                    resultContainer.innerHTML = `
                        <div class="alert alert-success">
                            Animation generated successfully!
                        </div>
                        <video src="${data.download_url}" controls class="w-100"></video>
                        <a href="${data.download_url}" download class="btn btn-success mt-2">
                            Download MP4
                        </a>
                    `;
                } else {
                    resultContainer.innerHTML = `
                        <div class="alert alert-danger">
                            Error: ${data.error || 'Animation generation failed'}
                        </div>
                    `;
                }
            } catch (error) {
                resultContainer.innerHTML = `
                    <div class="alert alert-danger">
                        Network error: ${error.message}
                    </div>
                `;
            }
        });
    </script>
</body>
</html>
