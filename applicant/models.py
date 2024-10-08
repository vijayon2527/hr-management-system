from django.db import models
from job.models import Skill
from users.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator
from job.models import Job
from employer.models import Employer
from applicant.managers import ApplicantManager, ApplicationManager
import os

def validate_file_size(file):
    limit = 2 * 1024 * 1024  # 2 MB
    if file.size > limit:
            raise ValidationError(f"File size should not exceed {limit / (1024 * 1024):.2f} MB. Current size: {file.size / (1024 * 1024):.2f} MB.")
 
class Applicant(models.Model):
    EXPERIENCE_INTERN_LEVEL = "Intern"
    EXPERIENCE_ENTRY_LEVEL = "Entry Level"
    EXPERIENCE_MID_LEVEL = "Mid Level"
    EXPERIENCE_SENIOR_LEVEL = "Senior Level"
    EXPERIENCE_MANAGEMENT_LEVEL = "Management Level"
    EXPERIENCE_EXECUTIVE_LEVEL = "Executive Level"

    EXPERIENCE_LEVEL_CHOICES = (
        (EXPERIENCE_INTERN_LEVEL, EXPERIENCE_INTERN_LEVEL),
        (EXPERIENCE_ENTRY_LEVEL, EXPERIENCE_ENTRY_LEVEL),
        (EXPERIENCE_MID_LEVEL, EXPERIENCE_MID_LEVEL),
        (EXPERIENCE_SENIOR_LEVEL, EXPERIENCE_SENIOR_LEVEL),
        (EXPERIENCE_MANAGEMENT_LEVEL, EXPERIENCE_MANAGEMENT_LEVEL),
        (EXPERIENCE_EXECUTIVE_LEVEL, EXPERIENCE_EXECUTIVE_LEVEL),
    )

    HIGHEST_EDUCATION_HIGH_SCHOOL = "High School"
    HIGHEST_EDUCATION_ASSOCIATE_DEGREE = "Associate Degree"
    HIGHEST_EDUCATION_BACHELORS_DEGREE = "Bachelor's Degree"
    HIGHEST_EDUCATION_MASTERS_DEGREE = "Master's Degree"
    HIGHEST_EDUCATION_DOCTORATE = "Doctorate"

    HIGHEST_EDUCATION_CHOICES = (
        (HIGHEST_EDUCATION_HIGH_SCHOOL, HIGHEST_EDUCATION_HIGH_SCHOOL),
        (HIGHEST_EDUCATION_ASSOCIATE_DEGREE, HIGHEST_EDUCATION_ASSOCIATE_DEGREE),
        (HIGHEST_EDUCATION_BACHELORS_DEGREE, HIGHEST_EDUCATION_BACHELORS_DEGREE),
        (HIGHEST_EDUCATION_MASTERS_DEGREE, HIGHEST_EDUCATION_MASTERS_DEGREE),
        (HIGHEST_EDUCATION_DOCTORATE, HIGHEST_EDUCATION_DOCTORATE),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='applicant',
        verbose_name="User"
    )
    resume = models.FileField(
        upload_to="resumes/%Y/%m/%d/",
        validators=[validate_file_size],
        help_text="Upload your resume in PDF or Word format.",
        verbose_name="Resume",
        null=False,
        blank=False
    )
    bio = models.TextField(
        blank=True,
        null=True,
        validators=[MaxLengthValidator(500)],
        help_text="A brief summary about yourself and your career (max 500 characters).",
        verbose_name="Bio"
    )
    current_job_title = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Your current job title.",
        verbose_name="Current Job Title"
    )
    skills = models.ManyToManyField(
        Skill,
        related_name='applicants',
        blank=True,
        help_text="Select the skills you possess.",
        verbose_name="Skills"
    )
    linkedin_profile = models.URLField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Link to your LinkedIn profile.",
        verbose_name="LinkedIn Profile"
    )
    github_profile = models.URLField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Link to your GitHub profile.",
        verbose_name="GitHub Profile"
    )
    portfolio_website = models.URLField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Link to your portfolio website.",
        verbose_name="Portfolio Website"
    )
    experience_level = models.CharField(
        max_length=50,
        choices=EXPERIENCE_LEVEL_CHOICES,
        blank=True,
        null=True,
        help_text="Select your overall experience level.",
        verbose_name="Experience Level"
    )
    years_of_experience = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Enter the total years of professional experience.",
        verbose_name="Years of Experience"
    )
    highest_education = models.CharField(
        max_length=100,
        choices=HIGHEST_EDUCATION_CHOICES,
        blank=True,
        null=True,
        help_text="Select your highest level of education.",
        verbose_name="Your Highest Education"
    )
    is_available_for_work = models.BooleanField(
        default=True,
        help_text="Are you currently looking for work?",
        verbose_name="Available for Work"
    )
    willing_to_relocate = models.BooleanField(
        default=False,
        help_text="Are you willing to relocate for a job?",
        verbose_name="Willing to Relocate"
    )
    desired_salary = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Expected salary (e.g., $60,000 per year).",
        verbose_name="Desired Salary"
    )
    notice_period = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Duration of notice before leaving (e.g., '2 weeks').",
        verbose_name="Notice Period"
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f'{self.user} - Applicant'
    
    objects = ApplicantManager()

    class Meta:
        verbose_name = 'Applicant Profile'
        verbose_name_plural = 'Applicant Profiles'

    @property
    def get_first_name(self):
        return self.user.first_name
    
    @property
    def get_last_name(self):
        return self.user.last_name
    
    @property
    def get_full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'
    
    @property
    def get_email(self):
        return self.user.email
    
    @property
    def get_mobile(self):
        return self.user.mobile
    
    @property
    def get_dob(self):
        return self.user.date_of_birth
    
    @property
    def get_address_line_1(self):
        return self.user.address_line_1
    
    @property
    def get_address_line_2(self):
        return self.user.address_line_2
    
    @property
    def get_city(self):
        return self.user.city
    
    @property
    def get_state(self):
        return self.user.state
    
    @property
    def get_country(self):
        return self.user.country
    
    @property
    def get_postal_code(self):
        return self.user.postal_code
    
    @property
    def get_linkedin_profile(self):
        return self.linkedin_profile if self.linkedin_profile else "Not available"
   
    @property
    def get_notice_period(self):
        return self.notice_period if self.notice_period else "Not available"
    
    def get_skills(self):
        return ', '.join(skill.name for skill in self.skills.all())

    def clean(self):
        super().clean()
        if self.resume:
            valid_extensions = ['.pdf', '.doc', '.docx']
            ext = os.path.splitext(self.resume.name)[1]
            if ext.lower() not in valid_extensions:
                raise ValidationError("Only PDF and Word documents are allowed for the resume.")

class Application(models.Model):
    APPLICATION_STATUS_PENDING = 'Pending'
    APPLICATION_STATUS_ACCEPTED = 'Accepted'
    APPLICATION_STATUS_REJECTED = 'Rejected'
    APPLICATION_STATUS_INTERVIEW = 'Interview'
    APPLICATION_STATUS_ON_HOLD = 'On Hold'

    APPLICATION_STATUS_CHOICES = (
        (APPLICATION_STATUS_PENDING, 'Pending'),
        (APPLICATION_STATUS_ACCEPTED, 'Accepted'),
        (APPLICATION_STATUS_REJECTED, 'Rejected'),
        (APPLICATION_STATUS_INTERVIEW, 'Interview'),
        (APPLICATION_STATUS_ON_HOLD, 'On Hold'),
    )
    applicant = models.ForeignKey(
        Applicant, 
        on_delete=models.CASCADE, 
        related_name='applications',
        verbose_name='Applicant',
    )
    job = models.ForeignKey(
        Job, 
        on_delete=models.CASCADE, 
        related_name='applications',
        verbose_name='Job',
    )
    applied_on = models.DateTimeField(
        auto_now_add=True, 
        verbose_name='Applied On',
    )
    status = models.CharField(
        max_length=20, 
        choices=APPLICATION_STATUS_CHOICES, 
        default=APPLICATION_STATUS_PENDING,
        verbose_name='Status',
    )
    cover_letter = models.TextField(
        blank=True, 
        null=True,
        verbose_name='Cover Letter',
        help_text='An optional letter to express your interest in the job and highlight your qualifications.'
    )
    notes = models.TextField(
        blank=True, 
        null=True,
        verbose_name='Recruiter Notes',
    )
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['applicant', 'job'], name='unique_job_application'),
        ]
        ordering = ['-applied_on']
        verbose_name = 'Application'
        verbose_name_plural = 'Applications'

    objects = ApplicationManager()

    def __str__(self):
        return f'{self.applicant.user.username} applied for {self.job.title}'

    @property
    def is_pending(self):
        return self.status == self.APPLICATION_STATUS_PENDING

    @property
    def get_status(self):
        return self.status
    
    @property
    def get_job(self):
        return self.job
    
    @property
    def get_job_title(self):
        return self.get_job.job_title
    
    @property
    def get_role(self):
        return self.get_job.role
    
    @property
    def get_company_name(self):
        return self.get_job.get_company_name
    
    @property
    def get_applicant(self):
        return self.applicant
    
    @property
    def get_user(self):
        return self.get_applicant.user
    
    @property
    def get_first_name(self):
        return self.get_user.first_name
    
    @property
    def get_last_name(self):
        return self.get_user.last_name
    
    @property
    def get_full_name(self):
        return f'{self.get_first_name} {self.get_last_name}'
    
    @property
    def get_mobile(self):
        return self.get_user.mobile
    
    @property
    def get_email(self):
        return self.get_user.email
    
    @property
    def get_notice_period(self):
        return self.get_applicant.notice_period
    
    @property
    def get_linkedin_profile(self):
        return self.get_applicant.linkedin_profile
    
    @property
    def get_resume(self):
        return self.get_applicant.resume
    
