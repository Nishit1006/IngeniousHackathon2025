from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.utils.crypto import get_random_string
from .models import LoanApplication
from accounts.models import FarmerProfile
from gis_data.models import Farmland

# Create your views here.

@login_required
def new_loan_application(request):
    """View for creating a new loan application."""
    context = {
        'title': 'Apply for a Loan - Farmer Credit Evaluation Tool',
        'active_page': 'new_loan',
    }
    
    # Process the form submission
    if request.method == 'POST':
        # Get form data
        loan_type = request.POST.get('loan_type')
        loan_amount = request.POST.get('loan_amount')
        loan_term = request.POST.get('loan_term')
        purpose = request.POST.get('purpose')
        farmland_id = request.POST.get('farmland')
        consent = request.POST.get('consent')
        
        # Validate the form data
        if not loan_type or not loan_amount or not loan_term or not purpose or not farmland_id or not consent:
            messages.error(request, 'Please fill out all required fields and provide consent.')
            return render(request, 'loan_application/new_application.html', context)
        
        # Get farmer profile for the current user
        try:
            farmer_profile = FarmerProfile.objects.get(user=request.user)
        except FarmerProfile.DoesNotExist:
            # Create farmer profile if it doesn't exist
            farmer_profile = FarmerProfile.objects.create(user=request.user)
        
        # Get farmland if it exists
        try:
            farmland = Farmland.objects.get(id=farmland_id)
        except Farmland.DoesNotExist:
            farmland = None
        
        # Generate a unique application number
        application_number = f"LA-{get_random_string(length=10, allowed_chars='0123456789')}"
        
        # Save to database
        loan_application = LoanApplication.objects.create(
            farmer=farmer_profile,
            farmland=farmland,
            application_number=application_number,
            loan_type=loan_type,
            amount_requested=loan_amount,
            term=loan_term,
            purpose=purpose,
            status='pending'
        )
        
        # Add a success message
        messages.success(request, f'Your loan application (#{application_number}) for ₹{loan_amount} has been submitted successfully! We will review your application shortly.')
        
        # Redirect to the applications list
        return redirect('loan_application:loan_applications_list')
    
    return render(request, 'loan_application/new_application.html', context)

@login_required
def loan_applications_list(request):
    """View for listing all loan applications for the current user."""
    # Get farmer profile for the current user
    try:
        farmer_profile = FarmerProfile.objects.get(user=request.user)
        # Get loan applications from database for the current user's farmer profile
        applications = LoanApplication.objects.filter(farmer=farmer_profile)
    except FarmerProfile.DoesNotExist:
        # If the user doesn't have a farmer profile, show no applications
        applications = []
    
    context = {
        'title': 'My Loan Applications - Farmer Credit Evaluation Tool',
        'active_page': 'applications',
        'applications': applications,
    }
    
    return render(request, 'loan_application/applications_list.html', context)

@login_required
def loan_application_detail(request, application_id):
    """View to display details of a specific loan application."""
    # Get the loan application if it exists and belongs to the current user
    application = get_object_or_404(
        LoanApplication, 
        id=application_id,
        farmer__user=request.user
    )
    
    context = {
        'title': f'Loan Application #{application.application_number} - Farmer Credit Evaluation Tool',
        'active_page': 'application_detail',
        'application': application,
    }
    
    return render(request, 'loan_application/application_detail.html', context)
