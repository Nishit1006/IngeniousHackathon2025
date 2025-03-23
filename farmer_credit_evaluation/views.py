from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.http import require_GET
from accounts.models import FarmerProfile
from credit_score.models import CreditScore
from gis_data.models import Farmland

# Frontend views
@require_GET
def home(request):
    """Home page view displaying the main landing page."""
    return render(request, 'home.html', {
        'title': 'Home - Farmer Credit Evaluation Tool',
        'active_page': 'home',
    })

@require_GET
def about(request):
    """About page view with information about the platform."""
    return render(request, 'about.html', {
        'title': 'About Us - Farmer Credit Evaluation Tool',
        'active_page': 'about',
    })

@require_GET
def contact(request):
    """Contact page view with contact form and information."""
    return render(request, 'contact.html', {
        'title': 'Contact Us - Farmer Credit Evaluation Tool',
        'active_page': 'contact',
    })

@require_GET
def privacy_policy(request):
    """Privacy policy page view."""
    return render(request, 'privacy_policy.html', {
        'title': 'Privacy Policy - Farmer Credit Evaluation Tool',
        'active_page': 'privacy',
    })

# Dashboard redirect view
@login_required
def dashboard_redirect(request):
    """Redirects users to the appropriate dashboard based on their user type."""
    user = request.user
    
    # Redirect based on user type
    if user.is_staff or user.is_superuser:
        return redirect('admin_dashboard')
    elif user.user_type == 'financial_institution':
        return redirect('institution_dashboard')
    else:  # Default to farmer dashboard
        return redirect('farmer_dashboard')

# Dashboard views
@login_required
def farmer_dashboard(request):
    """Dashboard view for farmers to manage their profile, land, and applications."""
    # Get user profile and verify it's a farmer
    user = request.user
    if user.user_type != 'farmer':
        return HttpResponseRedirect(reverse('home'))
    
    try:
        # Get farmer profile
        farmer_profile = FarmerProfile.objects.get(user=user)
        
        # Get current credit score
        credit_score = CreditScore.objects.filter(
            farmer=farmer_profile,
            is_current=True
        ).first()
        
        if credit_score:
            credit_score_value = credit_score.final_score
            credit_score_category = credit_score.get_risk_category()
            credit_score_date = credit_score.calculation_date
        else:
            credit_score_value = None
            credit_score_category = None
            credit_score_date = None
            
        # Get farmlands
        farmlands = Farmland.objects.filter(farmer=farmer_profile)
        
    except FarmerProfile.DoesNotExist:
        credit_score_value = None
        credit_score_category = None
        credit_score_date = None
        farmlands = []
    
    # Get farmer-specific data
    context = {
        'title': 'Farmer Dashboard - Farmer Credit Evaluation Tool',
        'active_page': 'dashboard',
        'user_type': 'farmer',
        'credit_score': credit_score_value,
        'credit_score_category': credit_score_category,
        'credit_score_category_display': credit_score_category if credit_score_category else "Not calculated",
        'credit_score_date': credit_score_date,
        'farmlands': farmlands,
    }
    
    return render(request, 'dashboard_farmer.html', context)

@login_required
def institution_dashboard(request):
    """Dashboard view for financial institutions to manage loan products and applications."""
    # Get user profile and verify it's a financial institution
    user = request.user
    if user.user_type != 'financial_institution':
        return HttpResponseRedirect(reverse('home'))
    
    # Get institution-specific data
    context = {
        'title': 'Institution Dashboard - Farmer Credit Evaluation Tool',
        'active_page': 'dashboard',
        'user_type': 'institution',
    }
    
    return render(request, 'dashboard_institution.html', context)

@login_required
def admin_dashboard(request):
    """Admin dashboard view for system administrators."""
    # Verify user is admin or superuser
    if not request.user.is_staff and not request.user.is_superuser:
        return HttpResponseRedirect(reverse('home'))
    
    context = {
        'title': 'Admin Dashboard - Farmer Credit Evaluation Tool',
        'active_page': 'dashboard',
        'user_type': 'admin',
    }
    
    return render(request, 'dashboard_admin.html', context)

# Credit score view
@login_required
def credit_score_view(request):
    """View for farmers to see their credit score details."""
    # Render a dedicated credit score page
    context = {
        'title': 'Credit Score - Farmer Credit Evaluation Tool',
        'active_page': 'credit_score',
    }
    return render(request, 'credit_score.html', context)
    
    # Commented out redirect approach
    # For now, we'll redirect to the farmer dashboard
    # return redirect('farmer_dashboard') 