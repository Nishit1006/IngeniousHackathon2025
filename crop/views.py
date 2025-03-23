from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import CropListing
from .forms import CropListingForm

def crop_marketplace(request):
    """View all available crop listings with optional search and sort functionality"""
    listings = CropListing.objects.filter(is_available=True)
    search_query = request.GET.get('search', '').strip()
    sort_by = request.GET.get('sort', 'recent')
    
    # Apply search filter if query exists
    if search_query:
        listings = listings.filter(
            Q(crop_name__icontains=search_query) |
            Q(description__icontains=search_query)
        ).distinct()
    
    # Apply sorting
    if sort_by == 'price_low':
        listings = listings.order_by('price_per_unit')
    elif sort_by == 'price_high':
        listings = listings.order_by('-price_per_unit')
    elif sort_by == 'quantity':
        listings = listings.order_by('-quantity')
    else:  # recent
        listings = listings.order_by('-created_at')
    
    context = {
        'listings': listings,
        'search_query': search_query,
        'sort_by': sort_by,
    }
    return render(request, 'crop/marketplace.html', context)

@login_required
def my_listings(request):
    """View user's own crop listings"""
    listings = CropListing.objects.filter(farmer=request.user)
    return render(request, 'crop/my_listings.html', {'listings': listings})

@login_required
def create_listing(request):
    """Create a new crop listing"""
    if request.method == 'POST':
        form = CropListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.farmer = request.user
            listing.save()
            messages.success(request, 'Your crop listing has been created successfully!')
            return redirect('crop:my_listings')
    else:
        form = CropListingForm()
    return render(request, 'crop/create_listing.html', {'form': form})

@login_required
def listing_detail(request, pk):
    """View details of a specific listing"""
    listing = get_object_or_404(CropListing, pk=pk)
    return render(request, 'crop/listing_detail.html', {'listing': listing})

@login_required
def toggle_listing(request, pk):
    """Toggle the availability of a listing"""
    listing = get_object_or_404(CropListing, pk=pk, farmer=request.user)
    listing.is_available = not listing.is_available
    listing.save()
    messages.success(request, f'Listing has been {"activated" if listing.is_available else "deactivated"}.')
    return redirect('crop:my_listings') 