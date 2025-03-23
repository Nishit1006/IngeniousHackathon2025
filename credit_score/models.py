from django.db import models
from django.conf import settings
from accounts.models import CustomUser, FarmerProfile
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal

class CreditScoreModel(models.Model):
    """Model for different credit score calculation models."""
    name = models.CharField(max_length=100)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class CreditScoreParameter(models.Model):
    """Parameters used in credit score calculation."""
    name = models.CharField(max_length=100)
    description = models.TextField()
    weight = models.DecimalField(max_digits=5, decimal_places=2)  # Weight in percentage
    model = models.ForeignKey(CreditScoreModel, on_delete=models.CASCADE, related_name='parameters')
    data_source = models.CharField(max_length=100)  # Where the data comes from
    min_value = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    max_value = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.weight}%)"
    
    class Meta:
        ordering = ['-weight']

class CreditScore(models.Model):
    """Model for storing farmer credit scores."""
    RISK_CATEGORIES = [
        ('low', 'Low Risk'),
        ('moderate', 'Moderate Risk'),
        ('high', 'High Risk'),
    ]

    farmer = models.ForeignKey(FarmerProfile, on_delete=models.CASCADE)
    calculation_date = models.DateTimeField(auto_now_add=True)
    is_current = models.BooleanField(default=True)
    
    # Component Scores (0-100)
    land_quality_score = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=70.00
    )
    weather_risk_score = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=70.00
    )
    crop_yield_score = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=70.00
    )
    market_demand_score = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=70.00
    )
    sustainability_score = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=70.00
    )
    
    # Final Score
    final_score = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        null=True,
        blank=True
    )
    
    # Additional Notes
    notes = models.TextField(blank=True, null=True)
    
    def calculate_final_score(self):
        """Calculate the weighted final score."""
        weights = {
            'land_quality': Decimal('0.30'),
            'weather_risk': Decimal('0.25'),
            'crop_yield': Decimal('0.20'),
            'market_demand': Decimal('0.15'),
            'sustainability': Decimal('0.10')
        }
        
        self.final_score = (
            self.land_quality_score * weights['land_quality'] +
            self.weather_risk_score * weights['weather_risk'] +
            self.crop_yield_score * weights['crop_yield'] +
            self.market_demand_score * weights['market_demand'] +
            self.sustainability_score * weights['sustainability']
        )
        return self.final_score

    def get_risk_category(self):
        """Return the risk category based on the final score."""
        if self.final_score >= 80:
            return 'Low Risk'
        elif self.final_score >= 60:
            return 'Moderate Risk'
        else:
            return 'High Risk'

    def save(self, *args, **kwargs):
        if not self.final_score:
            self.calculate_final_score()
            
        if self.is_current:
            # Set all other scores for this farmer to not current
            CreditScore.objects.filter(
                farmer=self.farmer,
                is_current=True
            ).exclude(pk=self.pk).update(is_current=False)
            
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-calculation_date']

class CreditScoreFactorValue(models.Model):
    """Values for each factor that contributed to a credit score."""
    credit_score = models.ForeignKey(CreditScore, on_delete=models.CASCADE, related_name='factor_values')
    parameter = models.ForeignKey(CreditScoreParameter, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    contribution = models.DecimalField(max_digits=10, decimal_places=2)  # Contribution to total score
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.parameter.name}: {self.value} (Contrib: {self.contribution})"
    
    class Meta:
        ordering = ['-contribution']
