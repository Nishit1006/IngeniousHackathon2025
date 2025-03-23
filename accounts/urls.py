from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet,
    FarmerProfileViewSet,
    FinancialInstitutionProfileViewSet,
    FarmerRegistrationView,
    FinancialInstitutionRegistrationView,
    CustomAuthToken,
    logout_view,
    user_profile,
    edit_profile,
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'farmers', FarmerProfileViewSet)
router.register(r'institutions', FinancialInstitutionProfileViewSet)

urlpatterns = [
    # Frontend URLs
    path('profile/', user_profile, name='user_profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    
    # API URLs
    path('api/', include(router.urls)),
    path('api/register/farmer/', FarmerRegistrationView.as_view(), name='farmer-register'),
    path('api/register/institution/', FinancialInstitutionRegistrationView.as_view(), name='institution-register'),
    path('api/login/', CustomAuthToken.as_view(), name='api-token-auth'),
    path('api/logout/', logout_view, name='api-token-logout'),
] 