from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, 
                                        BaseUserManager, 
                                        PermissionsMixin
                                        )

class UserManager(BaseUserManager):
    def _create_user(self, email, mobile, password=None, **extra_fields):
        if not mobile and not email:
            raise ValueError('Users must have either an email or mobile number')

        if email:
            email = self.normalize_email(email)
        mobile = self.normalize_mobile(mobile) if mobile else None
        user = self.model(email=email, mobile=mobile, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, mobile=None, password=None, **extra_fields):
        return self._create_user(email, mobile, password, **extra_fields)

    def create_superuser(self, email=None, mobile=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, mobile, password, **extra_fields)
    
    def normalize_mobile(self, mobile):
        # Remove whitespace and special characters
        normalized_mobile = ''.join(filter(str.isdigit, mobile))
        return normalized_mobile
    
class User(AbstractBaseUser, PermissionsMixin):
    SUPER_ADMIN = "Super Admin"
    EMPLOYER = "Employer"
    APPLICANT_USER = "Applicant User"
    APPLICATION_HANDLER ="Aplication Handler"

    USER_TYPE_CHOICES = (
        (SUPER_ADMIN, SUPER_ADMIN),
        (EMPLOYER, EMPLOYER),
        (APPLICANT_USER, APPLICANT_USER),
        (APPLICATION_HANDLER, APPLICATION_HANDLER),
    )

    INDIA = 'India'

    COUNTRY_CHOICES = (
        (INDIA, INDIA),
    )

    ANDHRA_PRASESH = 'Andhra Pradesh'
    ARUNACHAL_PRADESH = 'Arunachal Pradesh'
    ASSAM = 'Assam'
    BIHAR = 'Bihar'
    CHHATTISGARH = 'Chhattisgarh'
    GOA = 'Goa'
    GUJARAT = 'Gujarat'
    HARYANA = 'Haryana'
    HIMACHAL_PRADESH = 'Himachal Pradesh'
    JAMMU_AND_KASMIR = 'Jammu and Kashmir'
    JHARKHAND = 'Jharkhand'
    KARNATAKA = 'Karnataka'
    KERALA = 'Kerala'
    MADHYA_PRADESH = 'Madhya Pradesh'
    MAHARASHTRA = 'Maharashtra'
    MANIPUR = 'Manipur'
    MEGHALAYA = 'Meghalaya'
    MIZORAM = 'Mizoram'
    NAGALAND = 'Nagaland'
    ODISHA = 'Odisha'
    PUNJAB = 'Punjab'
    RAJASTHAN = 'Rajasthan'
    SIKKIM = 'Sikkim'
    TAMIL_NADU = 'Tamil Nadu'
    TELANGANA = 'Telangana'
    TRIPURA = 'Tripura'
    UTTAR_PRADESH = 'Uttar Pradesh'
    UTTARAKAND = 'Uttarakhand'
    WEST_BENGAL = 'West Bengal'
    ANDAMAN_AND_NICOBAR_ISLANDS = 'Andaman and Nicobar Island'
    CHANDIGARH = 'Chandigarh'
    DADRA_AND_NAGAR_HAVELI = 'Dadra and Nagar Haveli'
    DAMAN_AND_DIU = 'Daman and Diu'
    LAKSHADWEEP = 'Lakshadweep'
    NATIONAL_CAPITAL_TERRITORY_OF_DELHI = 'National Capital Territory of Delhi'
    PUDUCHERRY = 'Puducherry'
    
    STATE_CHOICES = (
        (ANDHRA_PRASESH, ANDHRA_PRASESH),
        (ARUNACHAL_PRADESH, ARUNACHAL_PRADESH),
        (ASSAM, ASSAM),
        (BIHAR, BIHAR),
        (CHHATTISGARH, CHHATTISGARH),
        (GOA, GOA),
        (GUJARAT, GUJARAT),
        (HARYANA, HARYANA),
        (HIMACHAL_PRADESH, HIMACHAL_PRADESH),
        (JAMMU_AND_KASMIR, JAMMU_AND_KASMIR),
        (JHARKHAND, JHARKHAND),
        (KARNATAKA, KARNATAKA),
        (KERALA, KERALA),
        (MADHYA_PRADESH, MADHYA_PRADESH),
        (MAHARASHTRA, MAHARASHTRA),
        (MANIPUR, MANIPUR),
        (MEGHALAYA, MEGHALAYA),
        (MIZORAM, MIZORAM),
        (NAGALAND, NAGALAND),
        (ODISHA, ODISHA),
        (PUNJAB, PUNJAB),
        (RAJASTHAN, RAJASTHAN),
        (SIKKIM, SIKKIM),
        (TAMIL_NADU, TAMIL_NADU),
        (TELANGANA, TELANGANA),
        (TRIPURA, TRIPURA),
        (UTTAR_PRADESH, UTTAR_PRADESH),
        (UTTARAKAND, UTTARAKAND),
        (WEST_BENGAL, WEST_BENGAL),
        (ANDAMAN_AND_NICOBAR_ISLANDS, ANDAMAN_AND_NICOBAR_ISLANDS),
        (CHANDIGARH, CHANDIGARH),
        (DADRA_AND_NAGAR_HAVELI, DADRA_AND_NAGAR_HAVELI),
        (DAMAN_AND_DIU, DAMAN_AND_DIU),
        (LAKSHADWEEP, LAKSHADWEEP),
        (NATIONAL_CAPITAL_TERRITORY_OF_DELHI,NATIONAL_CAPITAL_TERRITORY_OF_DELHI),
        (PUDUCHERRY, PUDUCHERRY)
    )
    email = models.EmailField(
        'email address', 
        unique=True, 
        null=True, 
        blank=True
        )
    first_name = models.CharField(
        max_length=255, 
        null=True, 
        blank=True
        )
    last_name = models.CharField(
        max_length=255, 
        null=True, 
        blank=True
        )
    mobile = models.CharField(
        'mobile number', 
        max_length=10, 
        unique=True, 
        null=True, 
        blank=True, 
        help_text="Enter your 10-digit mobile number without country code or spaces. Example: 8088870574."
        )
    profile_pic = models.ImageField(
        upload_to="user_profile_pics/%Y/%m/%d", 
        null=True, 
        blank=True
        )
    user_type = models.CharField(
        max_length=20, 
        choices=USER_TYPE_CHOICES, 
        default=APPLICANT_USER
        )
    date_of_birth = models.DateField(
        null=True,
        blank=True,
        verbose_name="Date of Birth",
        help_text="Enter your date of birth."
        )
    address_line_1 = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Address Line 1",
        help_text="Enter your main address."
        )
    address_line_2 = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Address Line 2",
        help_text="Enter an additional address or suite number, if applicable."
        )
    city = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="City",
        help_text="Enter the city where you live."
        )
    state = models.CharField(
        max_length=50,
        choices=STATE_CHOICES,
        default=KARNATAKA,
        null=True,
        blank=True,
        verbose_name="State",
        help_text="Select your state."
        )
    country = models.CharField(
        max_length=100,
        choices=COUNTRY_CHOICES,
        default=INDIA,
        blank=True,
        null=True,
        help_text="Your current country.",
        verbose_name="Country"
    )
    postal_code = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Postal Code",
        help_text="Enter the postal code for your area."
        )
    is_active = models.BooleanField(
        'active', 
        default=True
        )
    is_staff = models.BooleanField(
        'staff status', 
        default=False
        )
    date_joined = models.DateTimeField(
        'date joined', 
        auto_now_add=True
        )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email if self.email else str(self.mobile)

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self):
        return self.first_name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    
    def is_employer_profile_completed(self):
        from employer.models import Employer
        try:
            employer = Employer.objects.get(user=self)
        except Employer.DoesNotExist:
            return False

        return all([
            employer.company_name, 
            employer.company_website, 
            employer.contact_person_name, 
            employer.contact_number, 
            employer.company_address, 
            employer.city, 
            employer.state, 
            employer.country
        ])

    def is_applicant_profile_completed(self):
        from applicant.models import Applicant
        try:
            applicant = Applicant.objects.get(user=self)
        except Applicant.DoesNotExist:
            return False

        return all([
            self.first_name, 
            self.last_name, 
            self.date_of_birth, 
            self.address_line_1, 
            self.city, 
            self.state, 
            self.country,
            applicant.resume
        ])

    @property
    def is_profile_completed(self):
        if self.user_type == self.EMPLOYER:
            return self.is_employer_profile_completed()
        elif self.user_type == self.APPLICANT_USER:
            return self.is_applicant_profile_completed()
        return False