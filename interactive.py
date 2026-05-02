# interactive.py - Interactive price predictor
from predictor import HousingPredictor

def get_number(prompt, default, min_val=None, max_val=None):
    """Get a number from user input"""
    while True:
        try:
            value = input(f"{prompt} [{default}]: ")
            if value.strip() == "":
                value = default
            else:
                value = float(value)
            
            if min_val is not None and value < min_val:
                print(f"❌ Value must be at least {min_val}")
                continue
            if max_val is not None and value > max_val:
                print(f"❌ Value must be at most {max_val}")
                continue
            return value
        except ValueError:
            print("❌ Please enter a valid number")

print("=" * 60)
print("🏠 CALIFORNIA HOUSING PRICE PREDICTOR")
print("=" * 60)
print("\nEnter the details below (press Enter to use default values)\n")

# Load predictor
predictor = HousingPredictor()

# Get inputs
print("📍 LOCATION:")
lat = get_number("   Latitude (32-42)", 37.88, 32, 42)
lon = get_number("   Longitude (-125 to -114)", -122.23, -125, -114)

print("\n🏘️ NEIGHBORHOOD:")
med_inc = get_number("   Median Income ($100,000s)", 8.3252, 0, 15)
house_age = get_number("   House Age (years)", 41.0, 0, 100)
population = get_number("   Population", 322.0, 1, 5000)

print("\n🏠 HOUSE FEATURES:")
avg_rooms = get_number("   Average Rooms", 6.9841, 1, 20)
avg_bedrms = get_number("   Average Bedrooms", 1.0238, 0.5, 10)
avg_occup = get_number("   Average Occupancy", 2.5556, 0.5, 20)

# Make prediction
result = predictor.predict(
    MedInc=med_inc,
    HouseAge=house_age,
    AveRooms=avg_rooms,
    AveBedrms=avg_bedrms,
    Population=population,
    AveOccup=avg_occup,
    Latitude=lat,
    Longitude=lon
)

print("\n" + "=" * 60)
print("💰 PREDICTION RESULT")
print("=" * 60)
print(f"\n   Estimated Price: {result['formatted_price']}")
print(f"   ({result['price_100k']} in $100,000s)")
print("\n" + "=" * 60)