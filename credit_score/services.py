from decimal import Decimal
from .models import CreditScore
from gis_data.models import Farmland
from django.db.models import Avg

def calculate_land_quality_score(farmland):
    """Calculate land quality score (0-100) based on soil type and irrigation."""
    base_score = 70  # Default base score
    
    # Soil type scoring
    soil_scores = {
        'black': 100,
        'alluvial': 90,
        'red': 80,
        'laterite': 70,
        'sandy': 60,
        'clay': 75,
        'loam': 85
    }
    soil_score = soil_scores.get(farmland.soil_type.lower(), 70)
    
    # Irrigation scoring
    irrigation_score = 0
    if farmland.irrigation_source:
        irrigation_methods = [method.strip().lower() for method in farmland.irrigation_source.split(',')]
        if 'drip' in irrigation_methods:
            irrigation_score = 100
        elif 'sprinkler' in irrigation_methods:
            irrigation_score = 90
        elif 'canal' in irrigation_methods:
            irrigation_score = 80
        elif 'well' in irrigation_methods:
            irrigation_score = 70
        elif 'rain' in irrigation_methods:
            irrigation_score = 50
    
    # Calculate final land quality score
    final_score = (soil_score * 0.6) + (irrigation_score * 0.4)
    return min(max(final_score, 0), 100)  # Ensure score is between 0 and 100

def calculate_weather_risk_score(farmland):
    """Calculate weather risk score (0-100) based on location and season."""
    # Since we don't have weather data, we'll use a simplified scoring
    # based on irrigation availability
    base_score = 70  # Default moderate risk score
    
    if farmland.irrigation_source:
        irrigation_methods = [method.strip().lower() for method in farmland.irrigation_source.split(',')]
        
        # Better irrigation methods reduce weather risk
        if 'drip' in irrigation_methods:
            base_score += 20  # Very low weather risk
        elif 'sprinkler' in irrigation_methods:
            base_score += 15
        elif 'canal' in irrigation_methods:
            base_score += 10
        elif 'well' in irrigation_methods:
            base_score += 5
            
    return min(max(base_score, 0), 100)  # Ensure score is between 0 and 100

def calculate_crop_yield_score(farmer_profile):
    """Calculate crop yield score (0-100) based on available data."""
    # Since we don't have crop history data, return a default score
    return 70  # Default moderate score

def calculate_market_demand_score(farmer_profile):
    """Calculate market demand score (0-100) based on region."""
    # Since we don't have crop data, return a default score
    return 70  # Default moderate score

def calculate_sustainability_score(farmland):
    """Calculate sustainability score (0-100) based on farming practices."""
    base_score = 60  # Start with base score
    
    # Check irrigation methods
    if farmland.irrigation_source:
        irrigation_methods = [method.strip().lower() for method in farmland.irrigation_source.split(',')]
        if 'drip' in irrigation_methods:
            base_score += 20  # Drip irrigation is very sustainable
        elif 'sprinkler' in irrigation_methods:
            base_score += 15
        elif 'rainwater harvesting' in irrigation_methods:
            base_score += 10
            
    # Add more sustainability checks here as needed
    
    return min(max(base_score, 0), 100)  # Ensure score is between 0 and 100

def calculate_credit_score(farmer_profile):
    """Calculate overall credit score for a farmer considering all farmlands."""
    try:
        # Get all farmlands owned by the farmer
        farmlands = Farmland.objects.filter(farmer=farmer_profile)
        if not farmlands.exists():
            raise ValueError("No farmland registered for this farmer")
        
        total_area = Decimal('0')
        for farmland in farmlands:
            total_area += Decimal(str(farmland.area))
        
        # Initialize weighted scores
        weighted_land_quality = Decimal('0')
        weighted_weather_risk = Decimal('0')
        weighted_sustainability = Decimal('0')
        
        # Calculate weighted scores based on farmland area
        for farmland in farmlands:
            area_weight = Decimal(str(farmland.area)) / total_area
            
            # Calculate individual scores for this farmland
            land_quality = Decimal(str(calculate_land_quality_score(farmland)))
            weather_risk = Decimal(str(calculate_weather_risk_score(farmland)))
            sustainability = Decimal(str(calculate_sustainability_score(farmland)))
            
            # Add weighted scores
            weighted_land_quality += land_quality * area_weight
            weighted_weather_risk += weather_risk * area_weight
            weighted_sustainability += sustainability * area_weight
        
        # Calculate crop yield and market demand scores (these are farmer-level scores)
        crop_yield = Decimal(str(calculate_crop_yield_score(farmer_profile)))
        market_demand = Decimal(str(calculate_market_demand_score(farmer_profile)))
        
        # Create new credit score record
        credit_score = CreditScore.objects.create(
            farmer=farmer_profile,
            land_quality_score=weighted_land_quality,
            weather_risk_score=weighted_weather_risk,
            crop_yield_score=crop_yield,
            market_demand_score=market_demand,
            sustainability_score=weighted_sustainability,
            is_current=True,
            notes=f"Score calculated based on {farmlands.count()} farmland(s) with total area of {total_area} acres"
        )
        
        return credit_score
    except Exception as e:
        raise ValueError(f"Error calculating credit score: {str(e)}") 