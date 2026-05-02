# predictor.py - Simple housing price predictor
import pickle

class HousingPredictor:
    def __init__(self, model_path='artifacts/model.pkl'):
        """Load the trained model"""
        print("Loading model...")
        with open(model_path, 'rb') as f:
            self.model = pickle.load(f)
        print("✅ Model loaded successfully!")
    
    def predict(self, MedInc, HouseAge, AveRooms, AveBedrms, 
                Population, AveOccup, Latitude, Longitude):
        """
        Predict house price
        
        Returns: Price in dollars
        """
        # Create feature array in correct order
        features = [[
            MedInc, HouseAge, AveRooms, AveBedrms,
            Population, AveOccup, Latitude, Longitude
        ]]
        
        # Make prediction (returns price in $100,000s)
        price_100k = self.model.predict(features)[0]
        
        # Convert to dollars
        price_dollars = price_100k * 100000
        
        return {
            'price_100k': round(price_100k, 4),
            'price_dollars': round(price_dollars, 2),
            'formatted_price': f"${price_dollars:,.2f}"
        }

# Test it
if __name__ == "__main__":
    print("=" * 50)
    print("TESTING PREDICTOR")
    print("=" * 50)
    
    # Create predictor
    pred = HousingPredictor()
    
    # Test with sample house
    result = pred.predict(
        MedInc=8.3252,
        HouseAge=41.0,
        AveRooms=6.9841,
        AveBedrms=1.0238,
        Population=322.0,
        AveOccup=2.5556,
        Latitude=37.88,
        Longitude=-122.23
    )
    
    print(f"\n🏠 Sample House Prediction:")
    print(f"   Price: {result['formatted_price']}")
    print(f"   (or {result['price_100k']} in $100,000s)")