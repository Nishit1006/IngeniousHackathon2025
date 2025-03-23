from django.db import models
from django.conf import settings
from accounts.models import CustomUser, FarmerProfile

class Farmland(models.Model):
    """Model for farmer's land details."""
    farmer = models.ForeignKey(FarmerProfile, on_delete=models.CASCADE, related_name='farmlands')
    name = models.CharField(max_length=100)
    area = models.DecimalField(max_digits=10, decimal_places=2, help_text="Area in acres")
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    address = models.TextField(blank=True, null=True)
    soil_type = models.CharField(max_length=50, blank=True, null=True)
    irrigation_source = models.CharField(max_length=100, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    verification_date = models.DateField(blank=True, null=True)
    verified_by = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.area} acres)"

class WeatherData(models.Model):
    """Weather data for farmland locations."""
    farmland = models.ForeignKey(Farmland, on_delete=models.CASCADE, related_name='weather_data')
    date = models.DateField()
    temperature = models.DecimalField(max_digits=5, decimal_places=2, help_text="Temperature in Celsius")
    humidity = models.DecimalField(max_digits=5, decimal_places=2, help_text="Relative humidity in percentage")
    rainfall = models.DecimalField(max_digits=6, decimal_places=2, help_text="Rainfall in mm")
    wind_speed = models.DecimalField(max_digits=5, decimal_places=2, help_text="Wind speed in km/h")
    source = models.CharField(max_length=100, help_text="Source of weather data")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Weather for {self.farmland.name} on {self.date}"
    
    class Meta:
        ordering = ['-date']
        unique_together = ['farmland', 'date']

class SoilHealthData(models.Model):
    """Soil health data for farmland."""
    farmland = models.ForeignKey(Farmland, on_delete=models.CASCADE, related_name='soil_health_data')
    test_date = models.DateField()
    ph_level = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    nitrogen = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, help_text="Nitrogen in kg/ha")
    phosphorus = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, help_text="Phosphorus in kg/ha")
    potassium = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, help_text="Potassium in kg/ha")
    organic_matter = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text="Organic matter in percentage")
    moisture_content = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text="Moisture content in percentage")
    soil_health_index = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text="Overall soil health index (0-100)")
    test_lab = models.CharField(max_length=100, blank=True, null=True)
    report_file = models.FileField(upload_to='soil_reports/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Soil Health for {self.farmland.name} on {self.test_date}"
    
    class Meta:
        ordering = ['-test_date']

class CropHistory(models.Model):
    """Crop history for farmland."""
    farmland = models.ForeignKey(Farmland, on_delete=models.CASCADE, related_name='crop_history')
    crop_name = models.CharField(max_length=100)
    variety = models.CharField(max_length=100, blank=True, null=True)
    planting_date = models.DateField()
    harvest_date = models.DateField(blank=True, null=True)
    yield_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="Yield in quintals")
    yield_per_acre = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="Price per quintal in INR")
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    cost_of_production = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    profit = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.crop_name} on {self.farmland.name} ({self.planting_date})"
    
    def save(self, *args, **kwargs):
        """Calculate yield per acre, total revenue, and profit."""
        if self.yield_amount and self.farmland.area:
            self.yield_per_acre = self.yield_amount / self.farmland.area
        
        if self.yield_amount and self.selling_price:
            self.total_revenue = self.yield_amount * self.selling_price
        
        if self.total_revenue and self.cost_of_production:
            self.profit = self.total_revenue - self.cost_of_production
            
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['-planting_date']
        verbose_name_plural = "Crop histories"

class SatelliteImagery(models.Model):
    """Satellite imagery for farmland."""
    farmland = models.ForeignKey(Farmland, on_delete=models.CASCADE, related_name='satellite_imagery')
    image_date = models.DateField()
    image_url = models.URLField()
    image_type = models.CharField(max_length=50, choices=(
        ('rgb', 'RGB'),
        ('ndvi', 'NDVI - Vegetation Index'),
        ('evi', 'EVI - Enhanced Vegetation Index'),
        ('moisture', 'Soil Moisture'),
        ('other', 'Other'),
    ))
    source = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.image_type} imagery for {self.farmland.name} on {self.image_date}"
    
    class Meta:
        ordering = ['-image_date']
        verbose_name_plural = "Satellite imagery"
