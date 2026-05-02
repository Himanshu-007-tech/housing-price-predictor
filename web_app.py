# web_app.py - Web interface for housing price predictor
from predictor import HousingPredictor
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

# Initialize predictor
predictor = HousingPredictor()

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>🏠 CA Housing Price Predictor</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 700px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        h1 {
            text-align: center;
            color: #333;
            margin-bottom: 10px;
        }
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 30px;
        }
        .section {
            background: #f8f9fa;
            padding: 15px;
            margin: 15px 0;
            border-radius: 10px;
        }
        .section h3 {
            margin-top: 0;
            color: #667eea;
        }
        .input-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
            color: #555;
        }
        input {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 14px;
            box-sizing: border-box;
        }
        input:focus {
            outline: none;
            border-color: #667eea;
        }
        .row {
            display: flex;
            gap: 15px;
        }
        .row .input-group {
            flex: 1;
        }
        button {
            width: 100%;
            padding: 15px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            margin-top: 20px;
        }
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        .result {
            margin-top: 25px;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 10px;
            text-align: center;
            display: none;
        }
        .result.show {
            display: block;
            animation: fadeIn 0.5s;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .result h2 {
            color: white;
            margin: 0 0 10px 0;
            font-size: 14px;
        }
        .price {
            font-size: 32px;
            font-weight: bold;
            color: #ffd700;
        }
        .footer {
            text-align: center;
            margin-top: 20px;
            color: #999;
            font-size: 12px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🏠 California Housing Price Predictor</h1>
        <div class="subtitle">Enter house details to estimate price</div>
        
        <div class="section">
            <h3>📍 Location</h3>
            <div class="row">
                <div class="input-group">
                    <label>Latitude (32-42)</label>
                    <input type="number" step="0.01" id="lat" value="37.88">
                </div>
                <div class="input-group">
                    <label>Longitude (-125 to -114)</label>
                    <input type="number" step="0.01" id="lon" value="-122.23">
                </div>
            </div>
        </div>
        
        <div class="section">
            <h3>🏘️ Neighborhood</h3>
            <div class="input-group">
                <label>Median Income ($100,000s)</label>
                <input type="number" step="0.1" id="medinc" value="8.3252">
            </div>
            <div class="row">
                <div class="input-group">
                    <label>House Age (years)</label>
                    <input type="number" step="1" id="age" value="41">
                </div>
                <div class="input-group">
                    <label>Population</label>
                    <input type="number" step="10" id="pop" value="322">
                </div>
            </div>
        </div>
        
        <div class="section">
            <h3>🏠 House Features</h3>
            <div class="row">
                <div class="input-group">
                    <label>Avg Rooms</label>
                    <input type="number" step="0.1" id="rooms" value="6.9841">
                </div>
                <div class="input-group">
                    <label>Avg Bedrooms</label>
                    <input type="number" step="0.1" id="bedrms" value="1.0238">
                </div>
            </div>
            <div class="input-group">
                <label>Avg Occupancy</label>
                <input type="number" step="0.1" id="occup" value="2.5556">
            </div>
        </div>
        
        <button onclick="predict()">🔮 Predict Price</button>
        
        <div id="result" class="result">
            <h2>💰 Estimated Price</h2>
            <div class="price" id="price"></div>
        </div>
        
        <div class="footer">
            Based on California Housing Dataset | Linear Regression Model
        </div>
    </div>
    
    <script>
        async function predict() {
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
            
            const response = await fetch('/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            
            const result = await response.json();
            document.getElementById('price').innerHTML = result.formatted_price;
            document.getElementById('result').classList.add('show');
        }
    </script>
</body>
</html>
"""

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(HTML.encode())
    
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
        pass

print("=" * 60)
print("🌐 Starting Web Server...")
print("📱 Open your browser and go to: http://localhost:8080")
print("❌ Press Ctrl+C to stop")
print("=" * 60)

server = HTTPServer(('localhost', 8080), Handler)
server.serve_forever()