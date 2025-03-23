from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from .models import Farmland
from accounts.models import FarmerProfile
from .forms import FarmlandRegistrationForm

# Create your views here.

@login_required
def farmlands_list(request):
    """View to display all farmlands for the current user."""
    try:
        # Get the farmer profile for the current user
        farmer_profile = FarmerProfile.objects.get(user=request.user)
        # Get all farmlands for this farmer
        farmlands = Farmland.objects.filter(farmer=farmer_profile).order_by('-created_at')
    except FarmerProfile.DoesNotExist:
        farmlands = []
    
    context = {
        'title': 'My Farmlands - Farmer Credit Evaluation Tool',
        'active_page': 'farmlands',
        'farmlands': farmlands,
    }
    
    return render(request, 'gis_data/farmlands_list.html', context)

@login_required
def add_farmland(request):
    """View for adding a new farmland plot."""
    try:
        farmer_profile = FarmerProfile.objects.get(user=request.user)
    except FarmerProfile.DoesNotExist:
        # Create farmer profile if it doesn't exist
        farmer_profile = FarmerProfile.objects.create(user=request.user)

    if request.method == 'POST':
        try:
            # Process irrigation facilities
            irrigation_facilities = request.POST.getlist('irrigation_facilities')
            irrigation_source = ', '.join(irrigation_facilities) if irrigation_facilities else 'None'
            
            # Create new farmland object
            farmland = Farmland(
                farmer=farmer_profile,
                name=request.POST.get('name'),
                area=float(request.POST.get('area')),
                latitude=float(request.POST.get('latitude')),
                longitude=float(request.POST.get('longitude')),
                address=f"{request.POST.get('district', '')}, {request.POST.get('state', '')}",
                soil_type=request.POST.get('soil_type'),
                irrigation_source=irrigation_source
            )
            farmland.save()
            
            messages.success(request, f"Farmland '{farmland.name}' has been successfully registered.")
            return redirect('gis_data:farmlands_list')
        except Exception as e:
            messages.error(request, f"Error registering farmland: {str(e)}")
    
    context = {
        'title': 'Add Farmland - Farmer Credit Evaluation Tool',
        'active_page': 'add_farmland',
    }
    
    return render(request, 'gis_data/add_farmland.html', context)

@login_required
def farmland_detail(request, farmland_id):
    """View to display details of a specific farmland."""
    # Get the farmland object or return 404 if not found
    farmland = get_object_or_404(Farmland, id=farmland_id)
    
    # Check if the user owns this farmland
    if farmland.farmer.user != request.user:
        messages.error(request, "You don't have permission to view this farmland.")
        return redirect('gis_data:farmlands_list')
    
    if request.method == 'POST':
        try:
            # Process irrigation facilities
            irrigation_facilities = request.POST.getlist('irrigation_facilities')
            irrigation_source = ', '.join(irrigation_facilities) if irrigation_facilities else 'None'
            
            # Update farmland object
            farmland.name = request.POST.get('name')
            farmland.area = float(request.POST.get('area'))
            farmland.latitude = float(request.POST.get('latitude'))
            farmland.longitude = float(request.POST.get('longitude'))
            farmland.address = f"{request.POST.get('district', '')}, {request.POST.get('state', '')}"
            farmland.soil_type = request.POST.get('soil_type')
            farmland.irrigation_source = irrigation_source
            farmland.save()
            
            messages.success(request, f"Farmland '{farmland.name}' has been successfully updated.")
            return redirect('gis_data:farmland_detail', farmland_id=farmland.id)
        except Exception as e:
            messages.error(request, f"Error updating farmland: {str(e)}")
    
    # Convert irrigation_source string to list for template
    if farmland.irrigation_source:
        farmland.irrigation_source = [s.strip() for s in farmland.irrigation_source.split(',')]
    else:
        farmland.irrigation_source = []
    
    context = {
        'title': 'Farmland Details - Farmer Credit Evaluation Tool',
        'active_page': 'farmland_detail',
        'farmland': farmland,
        'edit_mode': request.GET.get('edit', False),
    }
    
    return render(request, 'gis_data/farmland_detail.html', context)

@login_required
def register_farmland(request):
    """View for registering farmland details."""
    try:
        farmer_profile = FarmerProfile.objects.get(user=request.user)
    except FarmerProfile.DoesNotExist:
        messages.error(request, "Farmer profile not found.")
        return redirect('home')
    
    if request.method == 'POST':
        form = FarmlandRegistrationForm(request.POST)
        if form.is_valid():
            farmland = form.save(commit=False)
            farmland.farmer = farmer_profile
            farmland.save()
            messages.success(request, "Farmland details registered successfully.")
            return redirect('/credit-score/')
    else:
        form = FarmlandRegistrationForm()
    
    context = {
        'title': 'Register Farmland - Farmer Credit Evaluation Tool',
        'active_page': 'register_farmland',
        'form': form,
    }
    
    return render(request, 'gis_data/register_farmland.html', context)
