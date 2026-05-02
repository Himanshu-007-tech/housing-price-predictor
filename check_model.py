# check_model.py - Simple model verification
import pickle
import os

print("=" * 50)
print("CHECKING YOUR MODEL")
print("=" * 50)

# Check if model exists
model_file = "artifacts/model.pkl"

if os.path.exists(model_file):
    print(f"✅ Model file found at: {model_file}")
    
    # Get file size
    size = os.path.getsize(model_file)
    print(f"📦 File size: {size} bytes")
    
    # Try to load
    try:
        with open(model_file, 'rb') as f:
            model = pickle.load(f)
        print("✅ Model loaded successfully!")
        print(f"📊 Model type: {type(model).__name__}")
        print("✅ Everything looks good!")
        
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        
else:
    print(f"❌ Model file NOT found at: {model_file}")
    print("Please make sure model.pkl is in the 'artifacts' folder")