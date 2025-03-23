from django.urls import path
from . import views

app_name = 'crop'

urlpatterns = [
    path('marketplace/', views.crop_marketplace, name='marketplace'),
    path('my-listings/', views.my_listings, name='my_listings'),
    path('create-listing/', views.create_listing, name='create_listing'),
    path('listing/<int:pk>/', views.listing_detail, name='listing_detail'),
    path('listing/<int:pk>/toggle/', views.toggle_listing, name='toggle_listing'),
] 