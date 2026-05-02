# final_test.py - Complete test for your model
import pickle
import numpy as np
import pandas as pd
import sklearn

print("=" * 50)
print("VERIFYING INSTALLATION")
print("=" * 50)

# Check packages
print("\n📦 Package versions:")
print(f"   NumPy: {np.__version__}")
print(f"   Pandas: {pd.__version__}")
print(f"   Scikit-learn: {sklearn.__version__}")

# Load and test model
print("\n🔧 Loading your model...")

with open('artifacts/model.pkl', 'rb') as f:
    model = pickle.load(f)

print("✅ Model loaded successfully!")
print(f"   Model type: {type(model).__name__}")

# Get feature names if available
if hasattr(model, 'feature_names_in_'):
    print(f"   Features: {list(model.feature_names_in_)}")

# Make a prediction
print("\n💰 Making test prediction...")

test_data = [[
    8.3252,   # MedInc
    41.0,     # HouseAge
    6.9841,   # AveRooms
    1.0238,   # AveBedrms
    322.0,    # Population
    2.5556,   # AveOccup
    37.88,    # Latitude
    -122.23   # Longitude
]]

prediction = model.predict(test_data)[0]

print(f"\n   Predicted price: ${prediction * 100000:,.2f}")
print(f"   (or {prediction:.4f} in $100,000s)")

print("\n✅ All tests passed! Your model is ready to use!")