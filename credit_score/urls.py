from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Import your views here
# from .views import CreditScoreViewSet, etc.

router = DefaultRouter()
# Register your viewsets here
# router.register(r'scores', CreditScoreViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # Add other URL patterns here
] 