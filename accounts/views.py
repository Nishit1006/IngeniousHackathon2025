from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib import messages
from django.urls import reverse

from rest_framework import viewsets, permissions, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

from .models import FarmerProfile, FinancialInstitutionProfile
from loan_application.models import LoanApplication
from .serializers import (
    UserSerializer, 
    FarmerProfileSerializer, 
    FinancialInstitutionProfileSerializer,
    UserRegistrationSerializer,
    FarmerProfileRegistrationSerializer,
    FinancialInstitutionRegistrationSerializer,
)

from allauth.account.views import SignupView
from allauth.account.forms import SignupForm

User = get_user_model()

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint to view users."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter users based on user type."""
        user_type = self.request.query_params.get('user_type', None)
        queryset = User.objects.all()
        
        if user_type:
            queryset = queryset.filter(user_type=user_type)
            
        return queryset

class FarmerProfileViewSet(viewsets.ModelViewSet):
    """API endpoint for farmer profiles."""
    queryset = FarmerProfile.objects.all()
    serializer_class = FarmerProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter profiles based on user permissions."""
        user = self.request.user
        
        # If the user is a farmer, they can only see their own profile
        if user.user_type == 'farmer':
            return FarmerProfile.objects.filter(user=user)
        
        # Admins and financial institutions can see all farmer profiles
        return FarmerProfile.objects.all()
    
    @action(detail=False, methods=['get'])
    def my_profile(self, request):
        """Get the profile of the logged-in farmer."""
        if request.user.user_type != 'farmer':
            return Response({"detail": "Only farmers can access this endpoint."}, 
                           status=status.HTTP_403_FORBIDDEN)
        
        try:
            profile = FarmerProfile.objects.get(user=request.user)
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
        except FarmerProfile.DoesNotExist:
            return Response({"detail": "Profile not found."}, 
                           status=status.HTTP_404_NOT_FOUND)

class FinancialInstitutionProfileViewSet(viewsets.ModelViewSet):
    """API endpoint for financial institution profiles."""
    queryset = FinancialInstitutionProfile.objects.all()
    serializer_class = FinancialInstitutionProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter profiles based on user permissions."""
        user = self.request.user
        
        # If the user is a financial institution, they can only see their own profile
        if user.user_type == 'financial_institution':
            return FinancialInstitutionProfile.objects.filter(user=user)
        
        # Admins can see all financial institution profiles
        return FinancialInstitutionProfile.objects.all()
    
    @action(detail=False, methods=['get'])
    def my_profile(self, request):
        """Get the profile of the logged-in financial institution."""
        if request.user.user_type != 'financial_institution':
            return Response({"detail": "Only financial institutions can access this endpoint."}, 
                           status=status.HTTP_403_FORBIDDEN)
        
        try:
            profile = FinancialInstitutionProfile.objects.get(user=request.user)
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
        except FinancialInstitutionProfile.DoesNotExist:
            return Response({"detail": "Profile not found."}, 
                           status=status.HTTP_404_NOT_FOUND)

class FarmerRegistrationView(generics.CreateAPIView):
    """API endpoint for farmer registration."""
    serializer_class = FarmerProfileRegistrationSerializer
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            farmer_profile = serializer.save()
            return Response({
                "user": UserSerializer(farmer_profile.user).data,
                "profile": FarmerProfileSerializer(farmer_profile).data,
                "message": "Farmer registered successfully."
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FinancialInstitutionRegistrationView(generics.CreateAPIView):
    """API endpoint for financial institution registration."""
    serializer_class = FinancialInstitutionRegistrationSerializer
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            institution_profile = serializer.save()
            return Response({
                "user": UserSerializer(institution_profile.user).data,
                "profile": FinancialInstitutionProfileSerializer(institution_profile).data,
                "message": "Financial institution registered successfully."
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomAuthToken(ObtainAuthToken):
    """Custom token auth with user data."""
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        
        user_data = UserSerializer(user).data
        
        # Get profile data based on user type
        profile_data = None
        if user.user_type == 'farmer':
            try:
                profile = FarmerProfile.objects.get(user=user)
                profile_data = FarmerProfileSerializer(profile).data
            except FarmerProfile.DoesNotExist:
                pass
        elif user.user_type == 'financial_institution':
            try:
                profile = FinancialInstitutionProfile.objects.get(user=user)
                profile_data = FinancialInstitutionProfileSerializer(profile).data
            except FinancialInstitutionProfile.DoesNotExist:
                pass
        
        return Response({
            'token': token.key,
            'user': user_data,
            'profile': profile_data
        })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """Logout and invalidate token."""
    try:
        request.user.auth_token.delete()
        return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@login_required
def user_profile(request):
    """View for user profile page."""
    user = request.user
    context = {
        'title': 'My Profile - Farmer Credit Evaluation Tool',
        'active_page': 'profile',
    }
    
    # Get profile data for display
    profile = None
    if user.user_type == 'farmer':
        try:
            profile = FarmerProfile.objects.get(user=user)
            context['profile'] = profile
            
            # Get additional data for farmer dashboard
            # Get latest credit score
            try:
                context['credit_score'] = profile.credit_scores.filter(is_current=True).first()
            except:
                pass
            
            # Get latest loan application
            try:
                context['latest_loan'] = profile.loan_applications.order_by('-created_at').first()
            except:
                pass
            
            # Get farmlands
            try:
                context['farmlands'] = profile.farmlands.all()
            except:
                pass
            
        except FarmerProfile.DoesNotExist:
            pass
    
    elif user.user_type == 'financial_institution':
        try:
            profile = FinancialInstitutionProfile.objects.get(user=user)
            context['profile'] = profile
            
            # Get additional data for financial institution dashboard
            # Get active loan products
            try:
                context['loan_products'] = profile.loan_products.filter(is_active=True)
            except:
                pass
            
            # Get recent loan applications
            try:
                context['recent_applications'] = LoanApplication.objects.filter(
                    loan_product__financial_institution=profile
                ).order_by('-created_at')[:5]
            except:
                pass
            
        except FinancialInstitutionProfile.DoesNotExist:
            pass
    
    return render(request, 'accounts/profile.html', context)

class CustomSignupView(SignupView):
    """Custom signup view to add success message and prevent automatic login."""
    
    def form_valid(self, form):
        # Save the user but don't log them in
        self.user = form.save(self.request)
        # Add success message
        messages.success(self.request, 'Registration successful! Please log in to continue.')
        # Redirect to login page
        return redirect('account_login')
