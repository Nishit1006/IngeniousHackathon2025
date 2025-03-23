from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Import your views
from .views import farmlands_list, add_farmland, farmland_detail, register_farmland

# Define the application namespace
app_name = 'gis_data'

router = DefaultRouter()
# Register your viewsets here
# router.register(r'farmlands', FarmlandViewSet)

urlpatterns = [
    # API endpoints
    path('', include(router.urls)),
    
    # Frontend URLs
    path('farmlands/', farmlands_list, name='farmlands_list'),
    path('farmlands/add/', add_farmland, name='add_farmland'),
    path('farmlands/<int:farmland_id>/', farmland_detail, name='farmland_detail'),
    path('register-farmland/', register_farmland, name='register_farmland'),
] 