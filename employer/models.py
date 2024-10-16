from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from users.models import User

def validate_file_size(file):
    limit = 2 * 1024 * 1024  # 2 MB
    if file.size > limit:
            raise ValidationError(f"File size should not exceed {limit / (1024 * 1024):.2f} MB. Current size: {file.size / (1024 * 1024):.2f} MB.")
    
class Employer(models.Model):
    COMPANY_SIZE_1_10 = '1-10'
    COMPANY_SIZE_11_50 = '11-50'
    COMPANY_SIZE_51_200 = '51-200'
    COMPANY_SIZE_201_500 = '201-500'
    COMPANY_SIZE_501_1000 = '501-1000'
    COMPANY_SIZE_1000_PLUS = '1000+'

    COMPANY_SIZE_CHOICES = (
        (COMPANY_SIZE_1_10, '1-10 employees'),
        (COMPANY_SIZE_11_50, '11-50 employees'),
        (COMPANY_SIZE_51_200, '51-200 employees'),
        (COMPANY_SIZE_201_500, '201-500 employees'),
        (COMPANY_SIZE_501_1000, '501-1000 employees'),
        (COMPANY_SIZE_1000_PLUS, '1000+ employees'),
    )
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='employer_profile'
    )
    company_name = models.CharField(
        max_length=200, 
        blank=True,
        null=True,
    )
    company_website = models.URLField(
        max_length=200
    )
    company_logo = models.ImageField(
        upload_to='company_logos/', 
        blank=True,
        null=True,
        validators=[validate_file_size],
    )
    contact_person_name = models.CharField(
        max_length=100
    )
    contact_number = models.CharField(
        'Mobile number', 
        max_length=10,  
        null=True, 
        blank=True, 
        help_text="Enter your 10-digit mobile number without country code or spaces. Example: 8088870574."
    )
    additional_contact_number = models.CharField(
        'Additional mobile number', 
        max_length=10, 
        null=True, 
        blank=True, 
        help_text="Enter your 10-digit mobile number without country code or spaces. Example: 8088870574."
    )
    company_address = models.TextField(
        blank=True, 
        null=True
    )
    city = models.CharField(
        max_length=100, 
        blank=True, 
        null=True
    )
    state = models.CharField(
        choices=User.STATE_CHOICES,
        max_length=100, 
        blank=True, 
        null=True
    )
    country = models.CharField(
        max_length=100, 
        blank=True, 
        null=True
    )
    zip_code = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )
    industry = models.CharField(
        max_length=100, 
        blank=True, 
        null=True
    )
    company_size = models.CharField(
        max_length=50,
        choices=COMPANY_SIZE_CHOICES,
        blank=True, 
        null=True
    )
    linkedin_url = models.URLField(
        max_length=200, 
        blank=True, 
        null=True
    )
    facebook_url = models.URLField(
        max_length=200, 
        blank=True, 
        null=True
    )
    twitter_url = models.URLField(
        max_length=200, 
        blank=True, 
        null=True
    )
    instagram_url = models.URLField(
        max_length=200, 
        blank=True, 
        null=True
    )
    is_verified = models.BooleanField(default=False)
    verified_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.company_name} - {self.user.email}'

    class Meta:
        verbose_name = 'Employer Profile'
        verbose_name_plural = 'Employer Profiles'
        ordering = ['company_name']

    def verify(self):
        self.is_verified = True
        self.verified_at = timezone.now()
        self.save()

    def get_active_jobs(self):
        return self.user.job_set.filter(is_active=True)
