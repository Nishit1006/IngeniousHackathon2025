from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Import your views
from .views import new_loan_application, loan_applications_list, loan_application_detail

# Define the application namespace
app_name = 'loan_application'

router = DefaultRouter()
# Register your viewsets here
# router.register(r'applications', LoanApplicationViewSet)

urlpatterns = [
    # Frontend URLs
    path('new/', new_loan_application, name='new_loan_application'),
    path('', loan_applications_list, name='loan_applications_list'),
    path('<int:application_id>/', loan_application_detail, name='application_detail'),
    
    # API endpoints
    path('api/', include(router.urls)),
] 