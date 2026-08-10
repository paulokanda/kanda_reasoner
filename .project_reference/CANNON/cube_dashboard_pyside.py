import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget,
    QStackedWidget, QLabel, QPushButton
)
from PySide6.QtCore import Qt
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtCore import QObject, Signal

# HTML/JS for the 3D cube (embedded as a string)
CUBE_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>3D Cube</title>
    <style>
        body { margin: 0; overflow: hidden; font-family: 'Segoe UI', sans-serif; }
        #info {
            position: absolute; bottom: 20px; left: 20px;
            background: rgba(0,0,0,0.6); color: white; padding: 10px 20px;
            border-radius: 8px; pointer-events: none; z-index: 10;
            font-size: 14px;
        }
        #hint {
            position: absolute; bottom: 20px; right: 20px;
            background: rgba(0,0,0,0.5); color: #ccc; padding: 8px 15px;
            border-radius: 20px; font-size: 12px; pointer-events: none;
        }
    </style>
</head>
<body>
    <div id="info">
        <strong>✨ 3D Cube Dashboard</strong><br>Click the cube → navigate
    </div>
    <div id="hint">
        🔄 rotating cube | click to go
    </div>

    <script type="importmap">
        {
            "imports": {
                "three": "https://unpkg.com/three@0.128.0/build/three.module.js",
                "three/addons/": "https://unpkg.com/three@0.128.0/examples/jsm/"
            }
        }
    </script>

    <script type="module">
        import * as THREE from 'three';

        // Setup scene
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x050b1a);
        scene.fog = new THREE.FogExp2(0x050b1a, 0.008);

        const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 1000);
        camera.position.set(2, 1.5, 3.5);
        camera.lookAt(0, 0, 0);

        const renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.shadowMap.enabled = true;
        document.body.appendChild(renderer.domElement);

        // Cube with metallic material
        const geometry = new THREE.BoxGeometry(1.2, 1.2, 1.2);
        const material = new THREE.MeshStandardMaterial({
            color: 0x3a86ff,
            emissive: 0x001133,
            roughness: 0.25,
            metalness: 0.85,
            emissiveIntensity: 0.6
        });
        const cube = new THREE.Mesh(geometry, material);
        cube.castShadow = true;
        scene.add(cube);

        // Wireframe edges
        const edgesGeo = new THREE.EdgesGeometry(geometry);
        const edgesMat = new THREE.LineBasicMaterial({ color: 0x88ccff });
        const wireframe = new THREE.LineSegments(edgesGeo, edgesMat);
        cube.add(wireframe);

        // Vertex sparkles
        const vertices = [
            [-0.6,-0.6,-0.6], [ 0.6,-0.6,-0.6], [ 0.6,-0.6, 0.6], [-0.6,-0.6, 0.6],
            [-0.6, 0.6,-0.6], [ 0.6, 0.6,-0.6], [ 0.6, 0.6, 0.6], [-0.6, 0.6, 0.6]
        ];
        const vertexPoints = vertices.map(v => new THREE.Vector3(v[0], v[1], v[2]));
        const pointsGeometry = new THREE.BufferGeometry().setFromPoints(vertexPoints);
        const pointsObj = new THREE.Points(pointsGeometry, new THREE.PointsMaterial({ color: 0xffaa66, size: 0.05 }));
        cube.add(pointsObj);

        // Lighting
        const ambientLight = new THREE.AmbientLight(0x404060);
        scene.add(ambientLight);
        const mainLight = new THREE.DirectionalLight(0xffffff, 1.2);
        mainLight.position.set(3, 5, 2);
        mainLight.castShadow = true;
        scene.add(mainLight);
        const fillLight = new THREE.PointLight(0x4466cc, 0.5);
        fillLight.position.set(0, -1, 0);
        scene.add(fillLight);
        const rimLight = new THREE.PointLight(0xffaa66, 0.6);
        rimLight.position.set(-1, 1, -2);
        scene.add(rimLight);

        // Floating particles
        const particleCount = 300;
        const particleGeometry = new THREE.BufferGeometry();
        const positions = new Float32Array(particleCount * 3);
        for (let i = 0; i < particleCount; i++) {
            const r = 1.6 + Math.random() * 0.8;
            const theta = Math.random() * Math.PI * 2;
            const phi = Math.acos(2 * Math.random() - 1);
            positions[i*3] = r * Math.sin(phi) * Math.cos(theta);
            positions[i*3+1] = r * Math.sin(phi) * Math.sin(theta);
            positions[i*3+2] = r * Math.cos(phi);
        }
        particleGeometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
        const particles = new THREE.Points(particleGeometry, new THREE.PointsMaterial({ color: 0x66ccff, size: 0.03, transparent: true, opacity: 0.5 }));
        scene.add(particles);

        // Grid floor
        const gridHelper = new THREE.GridHelper(8, 20, 0x88aaff, 0x335588);
        gridHelper.position.y = -0.9;
        gridHelper.material.transparent = true;
        gridHelper.material.opacity = 0.35;
        scene.add(gridHelper);

        // Click detection
        const raycaster = new THREE.Raycaster();
        const mouse = new THREE.Vector2();

        window.addEventListener('click', (event) => {
            mouse.x = (event.clientX / renderer.domElement.clientWidth) * 2 - 1;
            mouse.y = -(event.clientY / renderer.domElement.clientHeight) * 2 + 1;
            raycaster.setFromCamera(mouse, camera);
            const intersects = raycaster.intersectObject(cube, true);
            if (intersects.length > 0) {
                // Notify PySide via a custom event or URL change
                // We'll use a simple approach: navigate to a fake URL that PySide can intercept
                window.location.href = 'pyside://cube_clicked';
            }
        });

        // Animation loop
        let time = 0;
        function animate() {
            requestAnimationFrame(animate);
            time += 0.012;
            cube.rotation.y = time * 0.8;
            cube.rotation.x = Math.sin(time * 0.5) * 0.2;
            cube.rotation.z = Math.cos(time * 0.3) * 0.1;
            particles.rotation.y = time * 0.2;
            renderer.render(scene, camera);
        }
        animate();

        window.addEventListener('resize', () => {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        });
    </script>
</body>
</html>
"""


class Bridge(QObject):
    """Bridge for QWebChannel to communicate from JS to Python."""
    cubeClicked = Signal()

    def __init__(self):
        super().__init__()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide6 3D Cube Dashboard")
        self.resize(1024, 768)

        # Central widget with stacked layout (two pages)
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Page 1: The 3D cube
        self.cube_page = QWidget()
        cube_layout = QVBoxLayout(self.cube_page)
        self.web_view = QWebEngineView()
        # Load the HTML content
        self.web_view.setHtml(CUBE_HTML)
        cube_layout.addWidget(self.web_view)
        self.stack.addWidget(self.cube_page)

        # Page 2: Another page (example)
        self.other_page = QWidget()
        other_layout = QVBoxLayout(self.other_page)
        label = QLabel("You navigated to another page!")
        label.setStyleSheet("font-size: 24px; color: white; background-color: #2c3e50; padding: 20px;")
        label.setAlignment(Qt.AlignCenter)
        back_btn = QPushButton("Back to Cube")
        back_btn.clicked.connect(self.go_back)
        other_layout.addWidget(label)
        other_layout.addWidget(back_btn)
        self.other_page.setStyleSheet("background-color: #1a2a3a;")
        self.stack.addWidget(self.other_page)

        # Setup communication from JS to Python using QWebChannel
        self.bridge = Bridge()
        self.bridge.cubeClicked.connect(self.on_cube_clicked)
        self.channel = QWebChannel()
        self.channel.registerObject("bridge", self.bridge)
        self.web_view.page().setWebChannel(self.channel)

        # Inject the channel initialization into the HTML
        # We need to modify the HTML to use the channel. Let's append a script after the page loads.
        self.web_view.page().loadFinished.connect(self.inject_web_channel)

        # Show first page
        self.stack.setCurrentIndex(0)

    def inject_web_channel(self):
        """Add script to connect QWebChannel and override location change detection."""
        js = """
        // Connect to PySide bridge
        new QWebChannel(qt.webChannelTransport, function(channel) {
            window.pyBridge = channel.objects.bridge;
        });

        // Override location change to intercept pyside:// scheme
        (function() {
            var originalLocationSetter = Object.getOwnPropertyDescriptor(window, 'location').set;
            Object.defineProperty(window, 'location', {
                set: function(value) {
                    if (typeof value === 'string' && value.startsWith('pyside://')) {
                        // Trigger the bridge signal
                        if (window.pyBridge) {
                            window.pyBridge.cubeClicked.emit();
                        }
                        return;
                    }
                    originalLocationSetter.call(window, value);
                },
                get: function() { return originalLocationSetter ? originalLocationSetter.get() : window.location; }
            });
        })();
        """
        self.web_view.page().runJavaScript(js)

    def on_cube_clicked(self):
        """Handle cube click: switch to the other page."""
        self.stack.setCurrentIndex(1)

    def go_back(self):
        self.stack.setCurrentIndex(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())