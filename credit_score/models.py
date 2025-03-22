from django.db import models
from django.conf import settings
from accounts.models import CustomUser, FarmerProfile

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
    """Credit score for a farmer."""
    farmer = models.ForeignKey(FarmerProfile, on_delete=models.CASCADE, related_name='credit_scores')
    score = models.PositiveIntegerField()  # Score from 0-1000
    risk_category = models.CharField(max_length=20, choices=(
        ('very_low', 'Very Low Risk'),
        ('low', 'Low Risk'),
        ('medium', 'Medium Risk'),
        ('high', 'High Risk'),
        ('very_high', 'Very High Risk'),
    ))
    model_used = models.ForeignKey(CreditScoreModel, on_delete=models.SET_NULL, null=True, related_name='scores')
    is_current = models.BooleanField(default=True)  # Is this the current score
    calculation_date = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateField(null=True, blank=True)  # When the score expires
    
    def __str__(self):
        return f"{self.farmer.user.username}'s Score: {self.score}"
    
    def save(self, *args, **kwargs):
        """Set risk category based on score and set previous scores as not current."""
        if self.score >= 800:
            self.risk_category = 'very_low'
        elif self.score >= 650:
            self.risk_category = 'low'
        elif self.score >= 450:
            self.risk_category = 'medium'
        elif self.score >= 300:
            self.risk_category = 'high'
        else:
            self.risk_category = 'very_high'
            
        # If this is a new current score, set all other scores for this farmer to not current
        if self.is_current:
            CreditScore.objects.filter(farmer=self.farmer, is_current=True).update(is_current=False)
        
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
