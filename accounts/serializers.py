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
    
    def validate(self, data):
        if data['password'] != data['password_confirmation']:
            raise serializers.ValidationError({"password_confirmation": "Passwords don't match"})
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