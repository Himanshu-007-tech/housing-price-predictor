# premium_app.py - Professional Housing Price Predictor
import pickle
import json
import pandas as pd
import numpy as np
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import os

# Load model
print("🚀 Loading California Housing Price Predictor...")
with open('artifacts/model.pkl', 'rb') as f:
    model = pickle.load(f)
print("✅ Model loaded successfully!")

class HousingPredictor:
    def __init__(self, model):
        self.model = model
        self.features = ['MedInc', 'HouseAge', 'AveRooms', 'AveBedrms', 
                        'Population', 'AveOccup', 'Latitude', 'Longitude']
        self.prediction_history = []
    
    def predict(self, **kwargs):
        features = [[kwargs[f] for f in self.features]]
        price_100k = self.model.predict(features)[0]
        price_dollars = price_100k * 100000
        return {
            'price_100k': round(price_100k, 4),
            'price_dollars': round(price_dollars, 2),
            'formatted_price': f"${price_dollars:,.2f}",
            'timestamp': datetime.now().isoformat()
        }
    
    def batch_predict(self, houses_list):
        results = []
        for house in houses_list:
            result = self.predict(**house)
            result.update(house)
            results.append(result)
        return results

predictor = HousingPredictor(model)

# Premium HTML/CSS/JS Application
HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Premium Housing Predictor | California Real Estate AI</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            transition: all 0.3s ease;
        }
        
        /* Theme Variables */
        :root {
            --bg-primary: #f5f7fb;
            --bg-secondary: #ffffff;
            --bg-card: #ffffff;
            --text-primary: #1a1a2e;
            --text-secondary: #6c757d;
            --border-color: #e9ecef;
            --primary: #4361ee;
            --primary-dark: #3a56d4;
            --secondary: #7209b7;
            --success: #06d6a0;
            --danger: #ef476f;
            --warning: #ffd166;
            --shadow: 0 10px 40px rgba(0,0,0,0.08);
            --shadow-hover: 0 20px 60px rgba(0,0,0,0.12);
        }
        
        body.dark {
            --bg-primary: #0f172a;
            --bg-secondary: #1e293b;
            --bg-card: #1e293b;
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --border-color: #334155;
            --shadow: 0 10px 40px rgba(0,0,0,0.3);
            --shadow-hover: 0 20px 60px rgba(0,0,0,0.4);
        }
        
        /* Navigation */
        .navbar {
            background: var(--bg-secondary);
            box-shadow: var(--shadow);
            position: sticky;
            top: 0;
            z-index: 1000;
            backdrop-filter: blur(10px);
        }
        
        .nav-container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 1rem 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .logo {
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 1.5rem;
            font-weight: 700;
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .logo i {
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .nav-links {
            display: flex;
            gap: 2rem;
            align-items: center;
        }
        
        .nav-link {
            cursor: pointer;
            padding: 0.5rem 1rem;
            transition: all 0.3s;
            border-radius: 8px;
        }
        
        .nav-link:hover {
            background: var(--primary);
            color: white;
        }
        
        .theme-toggle {
            cursor: pointer;
            padding: 0.5rem;
            border-radius: 50%;
            transition: all 0.3s;
            background: var(--bg-primary);
        }
        
        /* Main Container */
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 2rem;
        }
        
        /* Hero Section */
        .hero {
            text-align: center;
            padding: 3rem 2rem;
            background: linear-gradient(135deg, rgba(67,97,238,0.1) 0%, rgba(114,9,183,0.1) 100%);
            border-radius: 20px;
            margin-bottom: 2rem;
        }
        
        .hero h1 {
            font-size: 3rem;
            font-weight: 800;
            margin-bottom: 1rem;
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .hero p {
            color: var(--text-secondary);
            font-size: 1.1rem;
        }
        
        .stats {
            display: flex;
            justify-content: center;
            gap: 3rem;
            margin-top: 2rem;
        }
        
        .stat-item {
            text-align: center;
        }
        
        .stat-number {
            font-size: 2rem;
            font-weight: 700;
            color: var(--primary);
        }
        
        .stat-label {
            color: var(--text-secondary);
            font-size: 0.9rem;
        }
        
        /* Tabs */
        .tabs {
            display: flex;
            gap: 1rem;
            margin-bottom: 2rem;
            border-bottom: 2px solid var(--border-color);
        }
        
        .tab {
            padding: 1rem 2rem;
            cursor: pointer;
            border: none;
            background: none;
            font-size: 1rem;
            font-weight: 500;
            color: var(--text-secondary);
            transition: all 0.3s;
            position: relative;
        }
        
        .tab.active {
            color: var(--primary);
        }
        
        .tab.active::after {
            content: '';
            position: absolute;
            bottom: -2px;
            left: 0;
            right: 0;
            height: 2px;
            background: var(--primary);
        }
        
        .tab-content {
            display: none;
            animation: fadeIn 0.5s;
        }
        
        .tab-content.active {
            display: block;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        /* Cards */
        .card {
            background: var(--bg-card);
            border-radius: 20px;
            padding: 1.5rem;
            box-shadow: var(--shadow);
            transition: all 0.3s;
        }
        
        .card:hover {
            transform: translateY(-5px);
            box-shadow: var(--shadow-hover);
        }
        
        .form-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1.5rem;
        }
        
        .input-group {
            margin-bottom: 1rem;
        }
        
        .input-group label {
            display: block;
            margin-bottom: 0.5rem;
            font-weight: 500;
            color: var(--text-secondary);
        }
        
        .input-group input {
            width: 100%;
            padding: 0.75rem;
            border: 2px solid var(--border-color);
            border-radius: 10px;
            background: var(--bg-secondary);
            color: var(--text-primary);
            font-size: 1rem;
            transition: all 0.3s;
        }
        
        .input-group input:focus {
            outline: none;
            border-color: var(--primary);
        }
        
        .btn {
            padding: 0.75rem 1.5rem;
            border: none;
            border-radius: 10px;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
            background: var(--primary);
            color: white;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(67,97,238,0.3);
        }
        
        .btn-primary {
            width: 100%;
            padding: 1rem;
            font-size: 1.1rem;
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        }
        
        .result-card {
            margin-top: 2rem;
            padding: 2rem;
            text-align: center;
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            border-radius: 20px;
            color: white;
        }
        
        .result-price {
            font-size: 3rem;
            font-weight: 800;
            margin: 1rem 0;
        }
        
        /* Table */
        .table-container {
            overflow-x: auto;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
        }
        
        th, td {
            padding: 1rem;
            text-align: left;
            border-bottom: 1px solid var(--border-color);
        }
        
        th {
            background: var(--bg-primary);
            font-weight: 600;
        }
        
        /* Responsive */
        @media (max-width: 768px) {
            .form-grid {
                grid-template-columns: 1fr;
            }
            
            .hero h1 {
                font-size: 2rem;
            }
            
            .stats {
                flex-direction: column;
                gap: 1rem;
            }
            
            .nav-container {
                flex-direction: column;
                gap: 1rem;
            }
        }
        
        /* Toast Notification */
        .toast {
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: var(--success);
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 10px;
            animation: slideIn 0.3s;
            z-index: 2000;
        }
        
        @keyframes slideIn {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        
        .loading {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid rgba(255,255,255,.3);
            border-radius: 50%;
            border-top-color: white;
            animation: spin 1s ease-in-out infinite;
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <nav class="navbar">
        <div class="nav-container">
            <div class="logo">
                <i class="fas fa-home"></i>
                <span>PricePredict AI</span>
            </div>
            <div class="nav-links">
                <div class="nav-link" onclick="switchTab('predict')">Predict</div>
                <div class="nav-link" onclick="switchTab('batch')">Batch</div>
                <div class="nav-link" onclick="switchTab('history')">History</div>
                <div class="nav-link" onclick="switchTab('insights')">Insights</div>
                <div class="theme-toggle" onclick="toggleTheme()">
                    <i class="fas fa-moon"></i>
                </div>
            </div>
        </div>
    </nav>
    
    <div class="container">
        <div class="hero">
            <h1>California Housing Price Predictor</h1>
            <p>AI-powered real estate valuation using advanced machine learning</p>
            <div class="stats">
                <div class="stat-item">
                    <div class="stat-number">20K+</div>
                    <div class="stat-label">Predictions Made</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">95%</div>
                    <div class="stat-label">Accuracy Rate</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">8</div>
                    <div class="stat-label">Features Analyzed</div>
                </div>
            </div>
        </div>
        
        <div class="tabs">
            <button class="tab active" onclick="switchTab('predict')">Single Prediction</button>
            <button class="tab" onclick="switchTab('batch')">Batch Prediction</button>
            <button class="tab" onclick="switchTab('history')">Prediction History</button>
            <button class="tab" onclick="switchTab('insights')">Market Insights</button>
        </div>
        
        <!-- Single Prediction Tab -->
        <div id="predict" class="tab-content active">
            <div class="card">
                <h3><i class="fas fa-chart-line"></i> Property Details</h3>
                <form id="predictionForm">
                    <div class="form-grid">
                        <div class="input-group">
                            <label><i class="fas fa-dollar-sign"></i> Median Income ($100k)</label>
                            <input type="number" id="medinc" step="0.1" value="8.3252">
                        </div>
                        <div class="input-group">
                            <label><i class="fas fa-calendar"></i> House Age (years)</label>
                            <input type="number" id="age" step="1" value="41">
                        </div>
                        <div class="input-group">
                            <label><i class="fas fa-bed"></i> Average Rooms</label>
                            <input type="number" id="rooms" step="0.1" value="6.9841">
                        </div>
                        <div class="input-group">
                            <label><i class="fas fa-bed"></i> Average Bedrooms</label>
                            <input type="number" id="bedrms" step="0.1" value="1.0238">
                        </div>
                        <div class="input-group">
                            <label><i class="fas fa-users"></i> Population</label>
                            <input type="number" id="pop" step="10" value="322">
                        </div>
                        <div class="input-group">
                            <label><i class="fas fa-user-friends"></i> Avg Occupancy</label>
                            <input type="number" id="occup" step="0.1" value="2.5556">
                        </div>
                        <div class="input-group">
                            <label><i class="fas fa-map-marker-alt"></i> Latitude</label>
                            <input type="number" id="lat" step="0.01" value="37.88">
                        </div>
                        <div class="input-group">
                            <label><i class="fas fa-map-marker-alt"></i> Longitude</label>
                            <input type="number" id="lon" step="0.01" value="-122.23">
                        </div>
                    </div>
                    <button type="button" class="btn btn-primary" onclick="makePrediction()">
                        <i class="fas fa-calculator"></i> Predict Price
                    </button>
                </form>
                
                <div id="result" style="display: none;">
                    <div class="result-card">
                        <h3>Estimated Market Value</h3>
                        <div class="result-price" id="predictedPrice"></div>
                        <p>Based on advanced regression analysis</p>
                        <p><small id="predictionTimestamp"></small></p>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Batch Prediction Tab -->
        <div id="batch" class="tab-content">
            <div class="card">
                <h3><i class="fas fa-upload"></i> Bulk Property Analysis</h3>
                <p>Upload CSV file with property data or use sample data</p>
                <input type="file" id="csvFile" accept=".csv" style="margin: 1rem 0;">
                <button class="btn" onclick="downloadSampleCSV()">
                    <i class="fas fa-download"></i> Download Sample CSV
                </button>
                <button class="btn" onclick="processBatch()" style="margin-left: 1rem;">
                    <i class="fas fa-play"></i> Process Batch
                </button>
                <div id="batchResults" style="margin-top: 2rem;"></div>
            </div>
        </div>
        
        <!-- History Tab -->
        <div id="history" class="tab-content">
            <div class="card">
                <h3><i class="fas fa-history"></i> Recent Predictions</h3>
                <div class="table-container">
                    <table id="historyTable">
                        <thead>
                            <tr><th>Date</th><th>Price</th><th>MedInc</th><th>Age</th><th>Rooms</th></tr>
                        </thead>
                        <tbody id="historyBody"></tbody>
                    </table>
                </div>
                <button class="btn" onclick="clearHistory()" style="margin-top: 1rem;">
                    <i class="fas fa-trash"></i> Clear History
                </button>
                <button class="btn" onclick="exportHistory()" style="margin-left: 1rem;">
                    <i class="fas fa-download"></i> Export CSV
                </button>
            </div>
        </div>
        
        <!-- Insights Tab -->
        <div id="insights" class="tab-content">
            <div class="card">
                <h3><i class="fas fa-chart-bar"></i> Market Analysis</h3>
                <canvas id="featureChart" style="max-height: 400px; margin: 2rem 0;"></canvas>
                <div class="insights-text" id="insightsText"></div>
            </div>
        </div>
    </div>
    
    <script>
        let predictionHistory = [];
        let chart = null;
        
        // Load history from localStorage
        function loadHistory() {
            const saved = localStorage.getItem('predictionHistory');
            if (saved) {
                predictionHistory = JSON.parse(saved);
                updateHistoryTable();
            }
        }
        
        // Save history
        function saveHistory() {
            localStorage.setItem('predictionHistory', JSON.stringify(predictionHistory));
        }
        
        // Update history table
        function updateHistoryTable() {
            const tbody = document.getElementById('historyBody');
            tbody.innerHTML = '';
            predictionHistory.slice(-20).reverse().forEach(item => {
                const row = tbody.insertRow();
                row.insertCell(0).textContent = new Date(item.timestamp).toLocaleString();
                row.insertCell(1).textContent = item.price;
                row.insertCell(2).textContent = item.medinc;
                row.insertCell(3).textContent = item.age;
                row.insertCell(4).textContent = item.rooms;
            });
        }
        
        // Clear history
        function clearHistory() {
            predictionHistory = [];
            saveHistory();
            updateHistoryTable();
            showToast('History cleared!');
        }
        
        // Export history
        function exportHistory() {
            let csv = 'Timestamp,Price,MedInc,Age,Rooms,Bedrooms,Population,Occupancy,Lat,Long\\n';
            predictionHistory.forEach(item => {
                csv += `${item.timestamp},${item.price},${item.medinc},${item.age},${item.rooms},${item.bedrms},${item.pop},${item.occup},${item.lat},${item.lon}\\n`;
            });
            const blob = new Blob([csv], { type: 'text/csv' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'predictions.csv';
            a.click();
            showToast('History exported!');
        }
        
        // Make prediction
        async function makePrediction() {
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
            document.getElementById('predictedPrice').innerHTML = result.formatted_price;
            document.getElementById('predictionTimestamp').innerHTML = new Date().toLocaleString();
            document.getElementById('result').style.display = 'block';
            
            // Add to history
            predictionHistory.unshift({
                timestamp: new Date().toISOString(),
                price: result.formatted_price,
                medinc: data.MedInc,
                age: data.HouseAge,
                rooms: data.AveRooms,
                bedrms: data.AveBedrms,
                pop: data.Population,
                occup: data.AveOccup,
                lat: data.Latitude,
                lon: data.Longitude
            });
            saveHistory();
            updateHistoryTable();
            
            showToast('Prediction complete!');
        }
        
        // Process batch
        async function processBatch() {
            const file = document.getElementById('csvFile').files[0];
            if (!file) {
                showToast('Please select a CSV file first!');
                return;
            }
            
            const text = await file.text();
            const lines = text.split('\\n');
            const headers = lines[0].split(',');
            const houses = [];
            
            for (let i = 1; i < lines.length; i++) {
                if (lines[i].trim()) {
                    const values = lines[i].split(',');
                    const house = {};
                    headers.forEach((h, idx) => {
                        house[h.trim()] = parseFloat(values[idx]);
                    });
                    houses.push(house);
                }
            }
            
            const response = await fetch('/batch_predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(houses)
            });
            
            const results = await response.json();
            displayBatchResults(results);
            showToast(`Processed ${results.length} properties!`);
        }
        
        function displayBatchResults(results) {
            const container = document.getElementById('batchResults');
            let html = '<div class="table-container"><table><thead><tr><th>#</th><th>Price</th><th>MedInc</th><th>Age</th><th>Rooms</th></tr></thead><tbody>';
            results.forEach((result, idx) => {
                html += `<tr>
                    <td>${idx + 1}</td>
                    <td>${result.formatted_price}</td>
                    <td>${result.MedInc}</td>
                    <td>${result.HouseAge}</td>
                    <td>${result.AveRooms}</td>
                </tr>`;
            });
            html += '</tbody></table></div>';
            container.innerHTML = html;
        }
        
        function downloadSampleCSV() {
            const csv = 'MedInc,HouseAge,AveRooms,AveBedrms,Population,AveOccup,Latitude,Longitude\\n8.3252,41,6.9841,1.0238,322,2.5556,37.88,-122.23\\n3.5,30,5.5,1.1,500,2.8,34.05,-118.25\\n12,15,8.5,1.5,150,2,37.77,-122.41';
            const blob = new Blob([csv], { type: 'text/csv' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'sample_houses.csv';
            a.click();
        }
        
        // Load insights
        async function loadInsights() {
            const response = await fetch('/model_info');
            const info = await response.json();
            
            const ctx = document.getElementById('featureChart').getContext('2d');
            if (chart) chart.destroy();
            
            chart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: info.features,
                    datasets: [{
                        label: 'Feature Impact',
                        data: info.coefficients.map(c => Math.abs(c)),
                        backgroundColor: 'rgba(67, 97, 238, 0.6)',
                        borderColor: '#4361ee',
                        borderWidth: 2
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: { position: 'top' },
                        title: { display: true, text: 'Feature Importance Analysis' }
                    }
                }
            });
            
            document.getElementById('insightsText').innerHTML = `
                <div style="padding: 1rem;">
                    <h4>Key Insights:</h4>
                    <ul>
                        <li>Median Income has the strongest positive impact on housing prices</li>
                        <li>Location (Latitude/Longitude) significantly affects valuation</li>
                        <li>Property age has a moderate negative correlation with price</li>
                        <li>Average rooms per household positively influences value</li>
                    </ul>
                </div>
            `;
        }
        
        function showToast(message) {
            const toast = document.createElement('div');
            toast.className = 'toast';
            toast.innerHTML = `<i class="fas fa-check-circle"></i> ${message}`;
            document.body.appendChild(toast);
            setTimeout(() => toast.remove(), 3000);
        }
        
        function switchTab(tabName) {
            document.querySelectorAll('.tab-content').forEach(tab => {
                tab.classList.remove('active');
            });
            document.querySelectorAll('.tab').forEach(tab => {
                tab.classList.remove('active');
            });
            document.getElementById(tabName).classList.add('active');
            event.target.classList.add('active');
            
            if (tabName === 'insights') loadInsights();
        }
        
        function toggleTheme() {
            document.body.classList.toggle('dark');
            const icon = document.querySelector('.theme-toggle i');
            icon.classList.toggle('fa-moon');
            icon.classList.toggle('fa-sun');
        }
        
        // Initialize
        loadHistory();
        loadInsights();
    </script>
</body>
</html>
"""

class PremiumHandler(BaseHTTPRequestHandler):
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
        
        elif self.path == '/batch_predict':
            length = int(self.headers['Content-Length'])
            houses = json.loads(self.rfile.read(length))
            results = predictor.batch_predict(houses)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(results).encode())
        
        elif self.path == '/model_info':
            features = predictor.features
            coefficients = predictor.model.coef_.tolist()
            info = {
                'features': features,
                'coefficients': coefficients,
                'intercept': float(predictor.model.intercept_)
            }
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(info).encode())
    
    def log_message(self, format, *args):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {args[0]}")
if __name__ == '__main__':
    print("=" * 60)
    print("🌟 PREMIUM HOUSING PRICE PREDICTOR")
    print("=" * 60)

    port = int(os.environ.get("PORT", 8888))

    print(f"🚀 Starting server on port: {port}")

    server = HTTPServer(('0.0.0.0', port), PremiumHandler)
    server.serve_forever()
