from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.core.validators import RegexValidator
from django.conf import settings

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError("Superuser must have is_staff=True.")
        if not extra_fields.get('is_superuser'):
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)
    
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=30, blank=True)
    phone_no = models.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                regex=r'^\d{10}$',
                message="Phone number must be exactly 10 digits."
            )
        ]
    )
    address=models.TextField(null=True,blank=True)
    college=models.CharField(max_length=150,null=True,blank=True)
    branch=models.CharField(max_length=50,null=True,blank=True)
    profile_pic=models.ImageField(upload_to="profile_pic/",null=True,blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name','phone_no']

    def __str__(self):
        return self.email
    

from datetime import timedelta
from django.utils.timezone import now

class Course(models.Model):
    DURATION_CHOICES = [
        ('1_month', '1 Month'),
        ('2_months', '2 Months'),
        ('3_months', '3 Months'),
        ('6_months', '6 Months'),
    ]
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    course_meterials=models.FileField(upload_to="course_material/",null=True,blank=True)
    course_image=models.ImageField(upload_to="course_image/",null=True,blank=True)
    course_video=models.FileField(upload_to="course_video/",null=True,blank=True)
    course_duration = models.CharField(max_length=50, choices=DURATION_CHOICES, null=True, blank=True)
    owner=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    accessible_until = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(null=True,blank=True)  # New field

    def save(self, *args, **kwargs):
        if self.course_duration:
            duration_mapping = {
                '1_month': timedelta(days=30),
                '2_months': timedelta(days=60),
                '3_months': timedelta(days=90),
                '6_months': timedelta(days=180),
            }
            self.accessible_until = now() + duration_mapping[self.course_duration]
        # Check if course has expired
        if self.accessible_until and now() > self.accessible_until:
            self.is_active = False
        super().save(*args, **kwargs)
    def __str__(self):
        return self.title



class EnrolledCourseUser(models.Model):
    # Many-to-many relationship between users and courses
    enrolled_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='enrollments',
        blank=True
    )
    enrolled_courses = models.ManyToManyField(
        'Course',
        related_name='enrolled_users',
        blank=True
    )


class ContactUs(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='contact_messages',
        help_text="Optional. Links to a registered user if available."
    )
    name = models.CharField(max_length=100, help_text="Name of the person submitting the message.")
    email = models.EmailField(help_text="Email address for follow-up.")
    phone_no = models.CharField(
        max_length=15, 
        blank=True, 
        null=True, 
        help_text="Optional. Contact phone number."
    )
    subject = models.CharField(max_length=255, help_text="Subject of the message.")
    message = models.TextField(help_text="Detailed message from the user.")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Date and time when the message was submitted.")
    is_resolved = models.BooleanField(default=False, help_text="Whether the message has been addressed.")

    def __str__(self):
        return f"{self.name} - {self.subject}"
    

class FAQ(models.Model):
    question = models.CharField(max_length=255, help_text="The question being asked.")
    answer = models.TextField(help_text="The answer to the question.")
    category = models.CharField(
        max_length=100, 
        blank=True, 
        null=True, 
        help_text="Optional. The category this FAQ belongs to (e.g., Billing, Account)."
    )
    is_active = models.BooleanField(default=True, help_text="Whether this FAQ is visible to users.")
    created_at = models.DateTimeField(auto_now_add=True, help_text="When this FAQ was created.")
    updated_at = models.DateTimeField(auto_now=True, help_text="When this FAQ was last updated.")

    class Meta:
        ordering = ['created_at']
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

    def __str__(self):
        return self.question