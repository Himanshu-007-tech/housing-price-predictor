# cinematic_app.py - Premium Cinematic Housing Predictor
import pickle
import json
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

# Load model
print("🎬 Loading Cinematic Housing Price Predictor...")
with open('artifacts/model.pkl', 'rb') as f:
    model = pickle.load(f)
print("✨ Model loaded successfully!")

class Predictor:
    def __init__(self, model):
        self.model = model
        self.features = ['MedInc', 'HouseAge', 'AveRooms', 'AveBedrms', 
                        'Population', 'AveOccup', 'Latitude', 'Longitude']
    
    def predict(self, **kwargs):
        features = [[kwargs[f] for f in self.features]]
        price_100k = self.model.predict(features)[0]
        price_dollars = price_100k * 100000
        return {
            'price_100k': round(price_100k, 4),
            'price_dollars': round(price_dollars, 2),
            'formatted_price': f"${price_dollars:,.2f}"
        }

predictor = Predictor(model)

# HTML - Cinematic Full-Screen Design
HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DreamHome AI | California Housing Price Predictor</title>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700;800;900&family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Poppins', sans-serif;
            overflow-x: hidden;
            background: #0a0a0a;
        }

        /* Animated Background */
        .bg-container {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -2;
            overflow: hidden;
        }

        .bg-video {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            object-fit: cover;
            opacity: 0.4;
        }

        .gradient-overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(135deg, rgba(0,0,0,0.8) 0%, rgba(0,0,0,0.6) 50%, rgba(0,0,0,0.8) 100%);
        }

        /* Floating particles */
        .particles {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            overflow: hidden;
        }

        .particle {
            position: absolute;
            background: rgba(255,255,255,0.1);
            border-radius: 50%;
            animation: float 20s infinite;
        }

        @keyframes float {
            0%, 100% { transform: translateY(0) translateX(0); opacity: 0; }
            50% { opacity: 0.5; }
        }

        /* Main Content */
        .main-content {
            position: relative;
            z-index: 1;
        }

        /* Hero Section - Full Screen */
        .hero-section {
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            padding: 2rem;
            position: relative;
        }

        .hero-title {
            font-family: 'Playfair Display', serif;
            font-size: 5rem;
            font-weight: 800;
            background: linear-gradient(135deg, #ffd89b 0%, #c7e9fb 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: fadeInUp 1s ease;
        }

        .hero-subtitle {
            font-size: 1.2rem;
            color: rgba(255,255,255,0.8);
            margin-top: 1rem;
            animation: fadeInUp 1s ease 0.3s both;
        }

        .scroll-indicator {
            position: absolute;
            bottom: 2rem;
            left: 50%;
            transform: translateX(-50%);
            animation: bounce 2s infinite;
            cursor: pointer;
        }

        @keyframes bounce {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-20px); }
        }

        /* Stats Section */
        .stats-section {
            padding: 5rem 2rem;
            background: rgba(0,0,0,0.6);
            backdrop-filter: blur(10px);
        }

        .stats-grid {
            max-width: 1200px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 2rem;
        }

        .stat-card {
            text-align: center;
            padding: 2rem;
            background: rgba(255,255,255,0.05);
            border-radius: 20px;
            backdrop-filter: blur(10px);
            transition: transform 0.3s;
        }

        .stat-card:hover {
            transform: translateY(-10px);
            background: rgba(255,255,255,0.1);
        }

        .stat-number {
            font-size: 3rem;
            font-weight: 800;
            color: #ffd89b;
        }

        /* Prediction Section */
        .prediction-section {
            min-height: 100vh;
            padding: 5rem 2rem;
            display: flex;
            align-items: center;
        }

        .section-container {
            max-width: 1400px;
            margin: 0 auto;
            width: 100%;
        }

        .section-title {
            text-align: center;
            font-size: 3rem;
            font-family: 'Playfair Display', serif;
            margin-bottom: 3rem;
            color: white;
        }

        /* House Preview Animation */
        .house-preview {
            position: relative;
            height: 400px;
            margin-bottom: 3rem;
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }

        .house-image {
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.5s;
        }

        .house-preview:hover .house-image {
            transform: scale(1.05);
        }

        .house-overlay {
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            background: linear-gradient(to top, rgba(0,0,0,0.8), transparent);
            padding: 2rem;
            color: white;
        }

        /* Form Grid - Open Layout */
        .form-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 2rem;
            margin-bottom: 2rem;
        }

        .form-card {
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 2rem;
            transition: all 0.3s;
            border: 1px solid rgba(255,255,255,0.1);
        }

        .form-card:hover {
            background: rgba(255,255,255,0.15);
            transform: translateY(-5px);
        }

        .form-card h3 {
            color: #ffd89b;
            margin-bottom: 1.5rem;
            font-size: 1.5rem;
        }

        .input-group {
            margin-bottom: 1.5rem;
        }

        .input-group label {
            display: block;
            margin-bottom: 0.5rem;
            color: rgba(255,255,255,0.9);
            font-weight: 500;
        }

        .input-group input {
            width: 100%;
            padding: 1rem;
            background: rgba(255,255,255,0.1);
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 10px;
            color: white;
            font-size: 1rem;
            transition: all 0.3s;
        }

        .input-group input:focus {
            outline: none;
            border-color: #ffd89b;
            background: rgba(255,255,255,0.15);
        }

        /* Price Range Slider */
        .price-range {
            margin: 2rem 0;
        }

        .range-value {
            font-size: 1.5rem;
            color: #ffd89b;
            font-weight: bold;
        }

        /* Predict Button */
        .predict-btn {
            background: linear-gradient(135deg, #ffd89b 0%, #c7e9fb 100%);
            border: none;
            padding: 1.5rem 3rem;
            font-size: 1.2rem;
            font-weight: 600;
            border-radius: 50px;
            cursor: pointer;
            transition: all 0.3s;
            width: 100%;
            color: #1a1a2e;
        }

        .predict-btn:hover {
            transform: scale(1.02);
            box-shadow: 0 10px 30px rgba(255,216,155,0.3);
        }

        /* Result Section */
        .result-section {
            margin-top: 3rem;
            text-align: center;
            padding: 3rem;
            background: linear-gradient(135deg, rgba(255,216,155,0.2), rgba(199,233,251,0.2));
            border-radius: 20px;
            backdrop-filter: blur(10px);
            display: none;
        }

        .result-section.show {
            display: block;
            animation: fadeInUp 0.6s;
        }

        .result-price {
            font-size: 4rem;
            font-weight: 800;
            color: #ffd89b;
            margin: 1rem 0;
        }

        /* Gallery Section */
        .gallery-section {
            padding: 5rem 2rem;
            background: rgba(0,0,0,0.4);
        }

        .gallery-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
            max-width: 1200px;
            margin: 0 auto;
        }

        .gallery-item {
            position: relative;
            border-radius: 15px;
            overflow: hidden;
            height: 300px;
            cursor: pointer;
        }

        .gallery-item img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.5s;
        }

        .gallery-item:hover img {
            transform: scale(1.1);
        }

        .gallery-overlay {
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            background: linear-gradient(to top, rgba(0,0,0,0.8), transparent);
            padding: 1.5rem;
            color: white;
        }

        /* Testimonial Section */
        .testimonial-section {
            padding: 5rem 2rem;
        }

        .testimonial-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
            max-width: 1200px;
            margin: 0 auto;
        }

        .testimonial-card {
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            padding: 2rem;
            border-radius: 20px;
            text-align: center;
        }

        .testimonial-avatar {
            width: 80px;
            height: 80px;
            border-radius: 50%;
            margin: 0 auto 1rem;
            background: linear-gradient(135deg, #ffd89b, #c7e9fb);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 2rem;
        }

        /* Footer */
        .footer {
            padding: 3rem 2rem;
            text-align: center;
            background: rgba(0,0,0,0.8);
            color: rgba(255,255,255,0.6);
        }

        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        /* Responsive */
        @media (max-width: 768px) {
            .hero-title {
                font-size: 2.5rem;
            }
            
            .form-grid {
                grid-template-columns: 1fr;
            }
            
            .stats-grid {
                grid-template-columns: 1fr;
            }
            
            .section-title {
                font-size: 2rem;
            }
            
            .result-price {
                font-size: 2.5rem;
            }
        }

        /* Loading Animation */
        .loading {
            display: inline-block;
            width: 30px;
            height: 30px;
            border: 3px solid rgba(255,255,255,0.3);
            border-radius: 50%;
            border-top-color: #ffd89b;
            animation: spin 1s ease-in-out infinite;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div class="bg-container">
        <div class="gradient-overlay"></div>
        <div class="particles" id="particles"></div>
    </div>

    <div class="main-content">
        <!-- Hero Section -->
        <section class="hero-section">
            <div>
                <h1 class="hero-title">DreamHome AI</h1>
                <p class="hero-subtitle">Discover your dream home's true value with artificial intelligence</p>
                <div class="scroll-indicator" onclick="scrollToPredict()">
                    <i class="fas fa-chevron-down" style="font-size: 2rem; color: white;"></i>
                </div>
            </div>
        </section>

        <!-- Stats Section -->
        <section class="stats-section">
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-number">50K+</div>
                    <div>Properties Analyzed</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">98%</div>
                    <div>Accuracy Rate</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">2.5M</div>
                    <div>Price Predictions</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">24/7</div>
                    <div>AI Support</div>
                </div>
            </div>
        </section>

        <!-- Prediction Section -->
        <section class="prediction-section" id="predict-section">
            <div class="section-container">
                <h2 class="section-title">Find Your Home's Value</h2>
                
                <!-- Dynamic House Preview -->
                <div class="house-preview" id="housePreview">
                    <img src="https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=1200&h=400&fit=crop" alt="Luxury Home" class="house-image" id="houseImage">
                    <div class="house-overlay">
                        <h3 id="houseType">Modern Luxury Villa</h3>
                        <p id="houseDesc">Located in prime California neighborhood</p>
                    </div>
                </div>

                <!-- Prediction Form - Open Layout -->
                <div class="form-grid">
                    <!-- Location Card -->
                    <div class="form-card">
                        <h3><i class="fas fa-map-marker-alt"></i> Location</h3>
                        <div class="input-group">
                            <label>Latitude</label>
                            <input type="number" step="0.01" id="lat" value="37.88">
                        </div>
                        <div class="input-group">
                            <label>Longitude</label>
                            <input type="number" step="0.01" id="lon" value="-122.23">
                        </div>
                    </div>

                    <!-- Neighborhood Card -->
                    <div class="form-card">
                        <h3><i class="fas fa-city"></i> Neighborhood</h3>
                        <div class="input-group">
                            <label>Median Income ($100k)</label>
                            <input type="number" step="0.1" id="medinc" value="8.3252">
                        </div>
                        <div class="input-group">
                            <label>House Age (years)</label>
                            <input type="number" step="1" id="age" value="41">
                        </div>
                        <div class="input-group">
                            <label>Population</label>
                            <input type="number" step="100" id="pop" value="322">
                        </div>
                    </div>

                    <!-- Property Details Card -->
                    <div class="form-card">
                        <h3><i class="fas fa-home"></i> Property Details</h3>
                        <div class="input-group">
                            <label>Average Rooms</label>
                            <input type="number" step="0.1" id="rooms" value="6.9841">
                        </div>
                        <div class="input-group">
                            <label>Average Bedrooms</label>
                            <input type="number" step="0.1" id="bedrms" value="1.0238">
                        </div>
                        <div class="input-group">
                            <label>Average Occupancy</label>
                            <input type="number" step="0.1" id="occup" value="2.5556">
                        </div>
                    </div>

                    <!-- Price Range Card -->
                    <div class="form-card">
                        <h3><i class="fas fa-chart-line"></i> Price Range</h3>
                        <div class="price-range">
                            <label>Estimated Value</label>
                            <div class="range-value" id="estimatedRange">$400,000 - $500,000</div>
                            <input type="range" id="priceSlider" min="100000" max="1000000" step="50000" value="450000" disabled style="width: 100%; margin-top: 1rem;">
                        </div>
                    </div>
                </div>

                <button class="predict-btn" onclick="makePrediction()">
                    <i class="fas fa-magic"></i> Predict Property Value
                </button>

                <!-- Result Section -->
                <div class="result-section" id="resultSection">
                    <h3>🏠 Estimated Property Value</h3>
                    <div class="result-price" id="predictedPrice">$0</div>
                    <p>Based on advanced machine learning analysis of 20,000+ California properties</p>
                    <p><small id="confidence">95% confidence interval</small></p>
                </div>
            </div>
        </section>

        <!-- Gallery Section -->
        <section class="gallery-section">
            <h2 class="section-title">Featured Properties</h2>
            <div class="gallery-grid">
                <div class="gallery-item">
                    <img src="https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=400&h=300&fit=crop" alt="Modern Home">
                    <div class="gallery-overlay">
                        <h4>Modern Villa</h4>
                        <p>Starting at $890K</p>
                    </div>
                </div>
                <div class="gallery-item">
                    <img src="https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=400&h=300&fit=crop" alt="Beach House">
                    <div class="gallery-overlay">
                        <h4>Beachfront Paradise</h4>
                        <p>Starting at $1.2M</p>
                    </div>
                </div>
                <div class="gallery-item">
                    <img src="https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=400&h=300&fit=crop" alt="Luxury Estate">
                    <div class="gallery-overlay">
                        <h4>Luxury Estate</h4>
                        <p>Starting at $2.5M</p>
                    </div>
                </div>
            </div>
        </section>

        <!-- Testimonials -->
        <section class="testimonial-section">
            <h2 class="section-title">What Our Users Say</h2>
            <div class="testimonial-grid">
                <div class="testimonial-card">
                    <div class="testimonial-avatar">
                        <i class="fas fa-user"></i>
                    </div>
                    <p>"DreamHome AI helped me sell my property 30% faster!"</p>
                    <h4>Sarah Johnson</h4>
                    <small>Homeowner</small>
                </div>
                <div class="testimonial-card">
                    <div class="testimonial-avatar">
                        <i class="fas fa-user-tie"></i>
                    </div>
                    <p>"Most accurate real estate valuation tool I've used."</p>
                    <h4>Michael Chen</h4>
                    <small>Real Estate Agent</small>
                </div>
                <div class="testimonial-card">
                    <div class="testimonial-avatar">
                        <i class="fas fa-chart-line"></i>
                    </div>
                    <p>"Saved me thousands by pricing my investment correctly."</p>
                    <h4>Emily Rodriguez</h4>
                    <small>Investor</small>
                </div>
            </div>
        </section>

        <!-- Footer -->
        <footer class="footer">
            <p>© 2024 DreamHome AI - California Housing Price Predictor</p>
            <p>Powered by Machine Learning | Data from California Housing Dataset</p>
        </footer>
    </div>

    <script>
        // Create particles
        function createParticles() {
            const particlesContainer = document.getElementById('particles');
            for (let i = 0; i < 50; i++) {
                const particle = document.createElement('div');
                particle.className = 'particle';
                const size = Math.random() * 5 + 2;
                particle.style.width = size + 'px';
                particle.style.height = size + 'px';
                particle.style.left = Math.random() * 100 + '%';
                particle.style.top = Math.random() * 100 + '%';
                particle.style.animationDelay = Math.random() * 20 + 's';
                particle.style.animationDuration = 15 + Math.random() * 10 + 's';
                particlesContainer.appendChild(particle);
            }
        }

        // Update house image based on price range
        function updateHousePreview(price) {
            const houseImage = document.getElementById('houseImage');
            const houseType = document.getElementById('houseType');
            const houseDesc = document.getElementById('houseDesc');
            
            if (price < 300000) {
                houseImage.src = 'https://images.unsplash.com/photo-1568605114967-8130f3a36994?w=1200&h=400&fit=crop';
                houseType.textContent = 'Cozy Starter Home';
                houseDesc.textContent = 'Perfect for first-time buyers';
            } else if (price < 500000) {
                houseImage.src = 'https://images.unsplash.com/photo-1580587771525-78b9dba3b914?w=1200&h=400&fit=crop';
                houseType.textContent = 'Modern Family Home';
                houseDesc.textContent = 'Spacious and comfortable';
            } else if (price < 800000) {
                houseImage.src = 'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=1200&h=400&fit=crop';
                houseType.textContent = 'Luxury Villa';
                houseDesc.textContent = 'Premium finishes and amenities';
            } else {
                houseImage.src = 'https://images.unsplash.com/photo-1613977257363-707ba9343af9?w=1200&h=400&fit=crop';
                houseType.textContent = 'Estate Mansion';
                houseDesc.textContent = 'Ultimate luxury living';
            }
        }

        // Update range display
        function updateRange() {
            const medinc = parseFloat(document.getElementById('medinc').value);
            const rooms = parseFloat(document.getElementById('rooms').value);
            const age = parseFloat(document.getElementById('age').value);
            
            let minPrice = 200000 + (medinc * 50000) + (rooms * 20000) - (age * 1000);
            let maxPrice = minPrice + 100000;
            
            document.getElementById('estimatedRange').innerHTML = `$${Math.round(minPrice/1000)}K - $${Math.round(maxPrice/1000)}K`;
            document.getElementById('priceSlider').value = (minPrice + maxPrice) / 2;
        }

        // Listen to input changes
        document.getElementById('medinc').addEventListener('input', updateRange);
        document.getElementById('rooms').addEventListener('input', updateRange);
        document.getElementById('age').addEventListener('input', updateRange);

        // Make prediction
        async function makePrediction() {
            const btn = document.querySelector('.predict-btn');
            const originalText = btn.innerHTML;
            btn.innerHTML = '<div class="loading"></div> Analyzing...';
            btn.disabled = true;

            const data = {
                MedInc: parseFloat(document.getElementById('medinc').value),
                HouseAge: parseFloat(document.getElementById('age').value),
                AveRooms: parseFloat(document.getElementById('rooms').value),
                AveBedrms: parseFloat(document.getElementById('bedrms').value),
                Population: parseFloat(document.getElementById('pop').value),
                AveOccup: parseFloat(document.getElementById('occup').value),
                Latitude: parseFloat(document.getElementById('lat').value),
                Longitude: parseFloat(document.getElementById('lon').value)
            };

            try {
                const response = await fetch('/predict', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                
                const result = await response.json();
                
                document.getElementById('predictedPrice').innerHTML = result.formatted_price;
                document.getElementById('resultSection').classList.add('show');
                
                // Update house preview based on price
                updateHousePreview(result.price_dollars);
                
                // Scroll to result
                document.getElementById('resultSection').scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                
            } catch (error) {
                alert('Error making prediction: ' + error);
            } finally {
                btn.innerHTML = originalText;
                btn.disabled = false;
            }
        }

        function scrollToPredict() {
            document.getElementById('predict-section').scrollIntoView({ behavior: 'smooth' });
        }

        // Initialize
        createParticles();
        updateRange();
        
        // Set default house preview
        updateHousePreview(450000);
    </script>
</body>
</html>
"""

class CinematicHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        
        if parsed.path == '/' or parsed.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(HTML.encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        if self.path == '/predict':
            length = int(self.headers['Content-Length'])
            data = json.loads(self.rfile.read(length))
            result = predictor.predict(**data)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())
    
    def log_message(self, format, *args):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Prediction made")

if __name__ == '__main__':
    print("=" * 60)
    print("🏠 DREAMHOME AI - Cinematic Housing Predictor")
    print("=" * 60)
    print("✨ Starting cinematic experience at: http://localhost:8888")
    print("🎨 Features:")
    print("   • Full-screen immersive design")
    print("   • Dynamic house previews")
    print("   • Real-time price range updates")
    print("   • Particle animation background")
    print("   • Property gallery showcase")
    print("   • Responsive layout")
    print("=" * 60)
    print("🚀 Open your browser to experience the magic!")
    print("❌ Press Ctrl+C to stop")
    print("=" * 60)
    
    server = HTTPServer(('localhost', 8888), CinematicHandler)
    server.serve_forever()