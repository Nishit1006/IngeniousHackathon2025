from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import FarmerProfile, FinancialInstitutionProfile

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'user_type', 'phone_number', 'date_joined']
        read_only_fields = ['date_joined']

class FarmerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = FarmerProfile
        fields = [
            'id', 'user', 'address', 'district', 'state', 'pincode', 
            'aadhar_number', 'pan_number', 'annual_income', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

class FinancialInstitutionProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = FinancialInstitutionProfile
        fields = [
            'id', 'user', 'institution_name', 'institution_type',
            'registration_number', 'headquarters_address', 'website',
            'established_year', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password_confirmation = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    
    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password_confirmation', 'user_type', 'phone_number']
    
    def validate_username(self, value):
        """Validate username."""
        if len(value) < 3:
            raise serializers.ValidationError("Username must be at least 3 characters long.")
        if not value.isalnum():
            raise serializers.ValidationError("Username can only contain letters and numbers.")
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already taken.")
        return value
    
    def validate_email(self, value):
        """Validate email."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email address is already registered.")
        return value
    
    def validate_password(self, value):
        """Validate password strength."""
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError("Password must contain at least one number.")
        if not any(char.isalpha() for char in value):
            raise serializers.ValidationError("Password must contain at least one letter.")
        return value
    
    def validate(self, data):
        """Validate password confirmation."""
        if data['password'] != data['password_confirmation']:
            raise serializers.ValidationError({
                "password_confirmation": "Passwords don't match. Please make sure both passwords are identical."
            })
        return data
    
    def create(self, validated_data):
        validated_data.pop('password_confirmation')
        user = User.objects.create_user(**validated_data)
        return user

class FarmerProfileRegistrationSerializer(serializers.ModelSerializer):
    user = UserRegistrationSerializer()
    
    class Meta:
        model = FarmerProfile
        fields = ['user', 'address', 'district', 'state', 'pincode', 'aadhar_number', 'pan_number', 'annual_income']
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_serializer = UserRegistrationSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        
        farmer_profile = FarmerProfile.objects.create(user=user, **validated_data)
        return farmer_profile

class FinancialInstitutionRegistrationSerializer(serializers.ModelSerializer):
    user = UserRegistrationSerializer()
    
    class Meta:
        model = FinancialInstitutionProfile
        fields = ['user', 'institution_name', 'institution_type', 'registration_number', 
                'headquarters_address', 'website', 'established_year']
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_serializer = UserRegistrationSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        
        institution_profile = FinancialInstitutionProfile.objects.create(user=user, **validated_data)
        return institution_profile 