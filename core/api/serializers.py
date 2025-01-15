from rest_framework import serializers
from django.utils.timezone import now
from core.models import *




from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = get_user_model()
        fields = ['email', 'full_name', 'phone_no', 'password', 'password2']
        extra_kwargs = {
            'email': {'required': True},
            'phone_no': {'required': True}
        }

    def validate(self, data):
        if data['password'] != data['password2']:
            raise ValidationError({"password": "Passwords must match."})
        return data

    def create(self, validated_data):
        # Remove password2 from validated_data
        validated_data.pop('password2', None)
        password = validated_data.pop('password')
        user = get_user_model().objects.create(**validated_data)
        user.set_password(password)  # Hash the password
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})







class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'full_name', 'phone_no', 'is_active', 'is_staff']
        read_only_fields = ['is_active', 'is_staff']

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = [
            'id',
            'title',
            'description',
            'price',
            'course_meterials',
            'course_image',
            'course_video',
            'course_duration',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']


User = get_user_model()  # To refer to the user model dynamically

class EnrolledCourseUserSerializer(serializers.ModelSerializer):
    # Use nested serializers to represent related models
    enrolled_users = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), many=True)
    enrolled_courses = CourseSerializer(many=True)

    class Meta:
        model = EnrolledCourseUser
        fields = ['id', 'enrolled_users', 'enrolled_courses']





class FAQSerializers(serializers.ModelSerializer):
    class Meta:
        model=FAQ
        fields=['id','question','answer','category','created_at']
        read_only_fields=['created_at']


