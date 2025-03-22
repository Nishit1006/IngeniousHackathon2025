"""
URL configuration for farmer_credit_evaluation project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# We'll use drf-yasg instead of the default docs
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from accounts.views import CustomSignupView

from . import views

schema_view = get_schema_view(
   openapi.Info(
      title="Farmer Credit Evaluation API",
      default_version='v1',
      description="API for the Farmer Credit Evaluation Tool",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@farmerkredit.local"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Authentication URLs
    path('accounts/signup/', CustomSignupView.as_view(), name='account_signup'),
    path('accounts/login/', include('allauth.account.urls')),
    path('accounts/', include('allauth.urls')),
    
    # Frontend pages
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    
    # Credit score page
    path('credit-score/', views.credit_score_view, name='credit_score'),
    
    # Dashboard redirect
    path('dashboard/', views.dashboard_redirect, name='dashboard'),
    
    # Dashboard pages
    path('dashboard/farmer/', views.farmer_dashboard, name='farmer_dashboard'),
    path('dashboard/institution/', views.institution_dashboard, name='institution_dashboard'),
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    
    # GIS data frontend pages
    path('gis-data/', include('gis_data.urls', namespace='gis_data')),
    
    # Loan application pages (frontend)
    path('loan-application/', include('loan_application.urls', namespace='loan_application')),
    
    # User account pages (frontend)
    path('accounts/', include('accounts.urls')),
    
    # API endpoints
    path('api/accounts/', include('accounts.urls')),
    path('api/credit-score/', include('credit_score.urls')),
    path('api/gis-data/', include('gis_data.urls')),
    
    # API Documentation with drf-yasg
    path('api/swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('api/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/docs/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # Django REST Framework browsable API
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
