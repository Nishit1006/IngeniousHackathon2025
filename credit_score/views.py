from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.models import FarmerProfile
from gis_data.models import Farmland
from .models import CreditScore
from .services import calculate_credit_score

@login_required
def credit_score_view(request):
    """View to display credit score and its components."""
    try:
        farmer_profile = FarmerProfile.objects.get(user=request.user)
    except FarmerProfile.DoesNotExist:
        messages.error(request, "Farmer profile not found.")
        return redirect('home')
    
    # Check if farmer has registered farmland
    farmland = Farmland.objects.filter(farmer=farmer_profile).first()
    if not farmland:
        messages.info(request, "Please register your farmland details to calculate your credit score.")
        return redirect('gis_data:register_farmland')
    
    # Get current credit score or calculate new one
    try:
        credit_score = CreditScore.objects.filter(
            farmer=farmer_profile,
            is_current=True
        ).first()
        
        if not credit_score or request.GET.get('recalculate'):
            credit_score = calculate_credit_score(farmer_profile)
            messages.success(request, "Credit score has been calculated successfully.")
    except Exception as e:
        messages.error(request, str(e))
        credit_score = None
    
    # Get historical scores
    historical_scores = CreditScore.objects.filter(
        farmer=farmer_profile,
        is_current=False
    ).order_by('-calculation_date')[:5]
    
    context = {
        'title': 'Credit Score - Farmer Credit Evaluation Tool',
        'active_page': 'credit_score',
        'credit_score': credit_score,
        'historical_scores': historical_scores,
        'risk_descriptions': {
            'low': 'Low Risk - Easy loan approval with low interest.',
            'moderate': 'Moderate Risk - Loan approval with moderate interest.',
            'high': 'High Risk - Needs improvement for better loan eligibility.'
        },
        'improvement_tips': {
            'land_quality_score': [
                'Implement soil conservation practices',
                'Upgrade irrigation systems',
                'Regular soil testing and treatment'
            ],
            'weather_risk_score': [
                'Install protective structures (e.g., greenhouses)',
                'Implement drip irrigation systems',
                'Consider crop insurance for weather-related risks'
            ],
            'crop_yield_score': [
                'Use high-quality seeds',
                'Follow recommended farming practices',
                'Maintain proper spacing between plants'
            ],
            'market_demand_score': [
                'Research market trends',
                'Consider growing high-demand crops',
                'Build relationships with local buyers'
            ],
            'sustainability_score': [
                'Adopt organic farming practices',
                'Implement water conservation methods',
                'Use renewable energy sources where possible'
            ]
        }
    }
    
    return render(request, 'credit_score/credit_score.html', context)
