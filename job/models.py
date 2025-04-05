from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
from .utils import generate_unique_slug
from job.managers import JobManager, SkillManager
from tinymce.models import HTMLField
from users.models import User
from super_admin.models import Industry, FunctionalArea, Role
class Skill(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = SkillManager()
    def __str__(self):
        return self.name
    
class Job(models.Model):    
    EMPLOYMENT_TYPE_FULL_TIME = 'Full time'
    EMPLOYMENT_TYPE_PART_TIME = 'Part time'
    EMPLOYMENT_TYPE_FREELANCING = 'Freelancing'
    EMPLOYMENT_TYPE_CONTRACT = 'Contract'
    EMPLOYMENT_TYPE_INTERNSHIP = 'Internship'
    EMPLOYMENT_TYPE_TEMPORARY = 'Temporary'
    EMPLOYMENT_TYPE_REMOTE = 'Remote'

    EMPLOYMENT_TYPE_CHOICES = (
        (EMPLOYMENT_TYPE_FULL_TIME, EMPLOYMENT_TYPE_FULL_TIME),
        (EMPLOYMENT_TYPE_PART_TIME, EMPLOYMENT_TYPE_PART_TIME),
        (EMPLOYMENT_TYPE_FREELANCING, EMPLOYMENT_TYPE_FREELANCING),
        (EMPLOYMENT_TYPE_CONTRACT, EMPLOYMENT_TYPE_CONTRACT),
        (EMPLOYMENT_TYPE_INTERNSHIP, EMPLOYMENT_TYPE_INTERNSHIP),
        (EMPLOYMENT_TYPE_TEMPORARY, EMPLOYMENT_TYPE_TEMPORARY),
        (EMPLOYMENT_TYPE_REMOTE, EMPLOYMENT_TYPE_REMOTE),
    )

    INDIA = 'India'

    COUNTRY_CHOICES = (
        (INDIA, INDIA),
    )

    SALARY_PERIOD_PER_YEAR = "Per Year"
    SALARY_PERIOD_PER_MONTH = "Per Month"
    SALARY_PERIOD_PER_WEEK = "Per Week"
    SALARY_PERIOD_PER_DAY = "Per Day"
    SALARY_PERIOD_PER_HOUR = "Per Hour"

    SALARY_PERIOD_CHOICES = (
        (SALARY_PERIOD_PER_YEAR, SALARY_PERIOD_PER_YEAR),
        (SALARY_PERIOD_PER_MONTH, SALARY_PERIOD_PER_MONTH),
        (SALARY_PERIOD_PER_WEEK, SALARY_PERIOD_PER_WEEK),
        (SALARY_PERIOD_PER_DAY, SALARY_PERIOD_PER_DAY),
        (SALARY_PERIOD_PER_HOUR, SALARY_PERIOD_PER_HOUR),
    )

    CURRENCY_INDIAN_RUPEE = "Indian Rupee (INR)"
    CURRENCY_USD = "US Dollar (USD)"
    CURRENCY_EUR = "Euro (EUR)"

    CURRENCY_CHOICES = (
        (CURRENCY_INDIAN_RUPEE, CURRENCY_INDIAN_RUPEE),
        (CURRENCY_USD, CURRENCY_USD),
        (CURRENCY_EUR, CURRENCY_EUR),
    )

    INDUSTRY_SOFTWARE = "IT-Software"
    INDUSTRY_FINANCE = "Finance"
    INDUSTRY_HEALTHCARE = "Healthcare"
    INDUSTRY_EDUCATION = "Education"
    INDUSTRY_RETAIL = "Retail"
    INDUSTRY_MANUFACTURING = "Manufacturing"
    INDUSTRY_CONSTRUCTION = "Construction"
    INDUSTRY_TELECOMMUNICATION = "Telecommunication"
    INDUSTRY_ENERGY = "Energy"
    INDUSTRY_MEDIA = "Media"
    INDUSTRY_AUTOMOTIVE = "Automotive"
    INDUSTRY_GOVERNMENT = "Government"
    INDUSTRY_AGRICULTURE = "Agriculture"

    INDUSTRY_CHOICES = (
        (INDUSTRY_SOFTWARE, INDUSTRY_SOFTWARE),
        (INDUSTRY_FINANCE, INDUSTRY_FINANCE),
        (INDUSTRY_HEALTHCARE, INDUSTRY_HEALTHCARE),
        (INDUSTRY_EDUCATION, INDUSTRY_EDUCATION),
        (INDUSTRY_RETAIL, INDUSTRY_RETAIL),
        (INDUSTRY_MANUFACTURING, INDUSTRY_MANUFACTURING),
        (INDUSTRY_CONSTRUCTION, INDUSTRY_CONSTRUCTION),
        (INDUSTRY_TELECOMMUNICATION, INDUSTRY_TELECOMMUNICATION),
        (INDUSTRY_ENERGY, INDUSTRY_ENERGY),
        (INDUSTRY_MEDIA, INDUSTRY_MEDIA),
        (INDUSTRY_AUTOMOTIVE, INDUSTRY_AUTOMOTIVE),
        (INDUSTRY_GOVERNMENT, INDUSTRY_GOVERNMENT),
        (INDUSTRY_AGRICULTURE, INDUSTRY_AGRICULTURE),
    )

    FUNCTIONAL_DEVELOPMENT = "Development"
    FUNCTIONAL_HR = "HR"
    FUNCTIONAL_SALES = "Sales"
    FUNCTIONAL_MARKETING = "Marketing"
    FUNCTIONAL_OPERATIONS = "Operations"
    FUNCTIONAL_FINANCE = "Finance"
    FUNCTIONAL_CUSTOMER_SERVICE = "Customer Service"
    FUNCTIONAL_PRODUCT_MANAGEMENT = "Product Management"
    FUNCTIONAL_RD = "Research and Development"
    FUNCTIONAL_ADMINISTRATION = "Administration"

    FUNCTIONAL_AREA_CHOICES = (
        (FUNCTIONAL_DEVELOPMENT, FUNCTIONAL_DEVELOPMENT),
        (FUNCTIONAL_HR, FUNCTIONAL_HR),
        (FUNCTIONAL_SALES, FUNCTIONAL_SALES),
        (FUNCTIONAL_MARKETING, FUNCTIONAL_MARKETING),
        (FUNCTIONAL_OPERATIONS, FUNCTIONAL_OPERATIONS),
        (FUNCTIONAL_FINANCE, FUNCTIONAL_FINANCE),
        (FUNCTIONAL_CUSTOMER_SERVICE, FUNCTIONAL_CUSTOMER_SERVICE),
        (FUNCTIONAL_PRODUCT_MANAGEMENT, FUNCTIONAL_PRODUCT_MANAGEMENT),
        (FUNCTIONAL_RD, FUNCTIONAL_RD),
        (FUNCTIONAL_ADMINISTRATION, FUNCTIONAL_ADMINISTRATION),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='jobs_posted',
        help_text="The employer/user posting the job."
    ) 
    slug = models.SlugField(
        max_length=255,
        blank=True,
        null=True,
        unique=True,
        help_text="Unique slug generated from the job title."
    )
    job_title = models.CharField(
        max_length=255,
        help_text="The title of the job position, e.g., 'Software Engineer'."
    )
    # industry = models.CharField(
    #     choices=INDUSTRY_CHOICES,
    #     default=INDUSTRY_SOFTWARE,
    #     max_length=100,
    #     help_text="Industry to which the job belongs, e.g., 'IT-Software', 'Finance'."
    # )
    # functional_area = models.CharField(
    #     choices=FUNCTIONAL_AREA_CHOICES,
    #     default=FUNCTIONAL_DEVELOPMENT,
    #     max_length=100,
    #     help_text="Functional area of the job, e.g., 'Development', 'HR'."
    # )
    # role = models.CharField(
    #     max_length=255,
    #     help_text="Specific role within the job, e.g., 'Backend Developer'."
    # )
    industry = models.ForeignKey(
        Industry,
        on_delete=models.CASCADE,
        related_name='jobs',
        help_text="Industry to which the job belongs.",
        verbose_name="Industry"
    )
    functional_area = models.ForeignKey(
        FunctionalArea,
        on_delete=models.CASCADE,
        related_name='jobs',
        help_text="Functional area of the job.",
        verbose_name="Functional Area"
    )
    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        related_name='jobs',
        help_text="Specific role within the job.",
        verbose_name="Role"
    )
    skills = models.ManyToManyField(
        Skill,
        related_name='jobs',
        blank=True,
        help_text="Skills required for the job (e.g., Python, JavaScript)."
    )
    job_description = HTMLField(
        help_text="Detailed job description, responsibilities, and qualifications."
    )
    min_experience = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0.0)],
        verbose_name="Minimum Experience (Years)",
        help_text="Enter the minimum years of experience required (e.g., 2.5 for two and a half years)."
    )

    max_experience = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(50.0)],
        verbose_name="Maximum Experience (Years)",
        help_text="Enter the maximum years of experience required (e.g., 5.0 for five years)."
    )

    min_salary = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        verbose_name="Minimum Salary (INR)",
        help_text="Enter the minimum monthly salary offered in INR (e.g., '50000' for 50,000)."
    )

    max_salary = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        verbose_name="Maximum Salary (INR)",
        help_text="Enter the maximum monthly salary offered in INR (e.g., '70000' for 70,000)."
    )

    salary_currency = models.CharField(
        choices=CURRENCY_CHOICES,
        max_length=50,
        default=CURRENCY_INDIAN_RUPEE,
        help_text="Currency of the salary, e.g., 'INR', 'USD'."
    )
    salary_period = models.CharField(
        max_length=10,
        choices=SALARY_PERIOD_CHOICES,
        default=SALARY_PERIOD_PER_MONTH,
        help_text="Salary period, e.g., 'Per Year', 'Per Month'."
    )
    no_of_openings = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1)],
        help_text="Number of openings available for this position."
    )
    qualification = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Qualification required for the job (optional)."
    )
    employment_type = models.CharField(max_length=50, 
                                        choices=EMPLOYMENT_TYPE_CHOICES, 
                                        default=EMPLOYMENT_TYPE_FULL_TIME,
                                        help_text="Type of employment: Full time, Part time, etc."
                                        )
    country = models.CharField(
        choices=COUNTRY_CHOICES,
        default=INDIA,
        max_length=50, 
    )
    state = models.CharField(
        choices=User.STATE_CHOICES,
        default=User.KARNATAKA,
        max_length=50,
        help_text="State where the job is located (optional)."
    )
    city = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text="City where the job is located."
    )
    address = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Enter the specific address or office location, e.g., 'Building 3, Floor 5'."
    )
    zipcode = models.CharField(
        max_length=6,
        null=True,
        blank=True,
        help_text="6-digit PIN code for the specific location."
    )
    remote_possible = models.BooleanField(
        default=False,
        help_text="Indicates if remote work is allowed for this job."
    )
    is_flexible = models.BooleanField(
        default=False,
        help_text="Indicates if flexible working hours are available."
    )
    visa_sponsorship = models.BooleanField(
        default=False,
        help_text="Indicates if visa sponsorship is offered for this job."
    )
    relocation_support = models.BooleanField(
        default=False,
        help_text="Indicates if relocation support is available."
    )
    benefits = HTMLField(
        blank=True,
        null=True,
        help_text="List of benefits provided (e.g., Health insurance, Retirement plans)."
    )
    perks = HTMLField(
        blank=True,
        null=True,
        help_text="Additional perks offered by the company (e.g., Gym membership)."
    )

    visit_count = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Number of times the job post has been viewed."
    )
    job_applied_count = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Number of candidates who have applied for the job."
    )
    featured = models.BooleanField(
        default=False,
        help_text="Mark this job as featured for extra visibility."
    )
    publish = models.BooleanField(
        default=False,
        help_text="Indicates if the job post is published and visible."
    )
    recommended_job = models.BooleanField(
        default=False,
        help_text="Mark this job as recommended for users."
    )
    is_expired = models.BooleanField(
        default=False,
        help_text="Mark the job as expired after the application deadline."
    )
    application_deadline = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Deadline for applying to the job."
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        help_text="The date when the job was uploaded."
    )
    published_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="The date when the job was published."
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        null=True,
        help_text="The date when the job post was last updated."
    )
    expired_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="The date when the job post will expire."
    )

    objects = JobManager()

    class Meta:
        verbose_name = 'Job Post'
        verbose_name_plural = 'Job Posts'
        ordering = ['-id']

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = generate_unique_slug(Job, self.job_title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.job_title
    
    @property
    def get_company_name(self):
        from employer.models import Employer
        return Employer.objects.filter(user=self.user).first().company_name
    
    @property
    def get_all_skills(self):
        return self.skills.all()
    
    @property
    def is_remote(self):
        return self.employment_type == self.EMPLOYMENT_TYPE_REMOTE or self.remote_possible
    
    @property
    def get_salary(self):
        return f"{self.min_salary} to {self.max_salary} {self.salary_currency} {self.salary_period}" 
    
    @property
    def get_experience(self):
        if self.min_experience is None or self.max_experience is None:
            return None
        return f"{self.min_experience} to {self.max_experience} years"

 
    