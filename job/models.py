from django.db import models

from django.utils.text import slugify
from .utils import generate_unique_slug
from django.urls import reverse
from job.managers import JobApplicantManager, JobManager, SkillManager
from tinymce.models import HTMLField
from users.models import User
from employer.models import Employer

class Skill(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = SkillManager()
    def __str__(self):
        return self.name
    
class Job(models.Model):
    EMPLOYEMENT_TYPE_FULL_TIME = 'Full time'
    EMPLOYEMENT_TYPE_PART_TIME = 'Part time'
    EMPLOYEMENT_TYPE_FREELANCING = 'Freelancing'
    EMPLOYEMENT_TYPE_CONTRACT = 'Contract'

    EMPLOYEMENT_TYPE_CHOICES = (
        (EMPLOYEMENT_TYPE_FULL_TIME, EMPLOYEMENT_TYPE_FULL_TIME),
        (EMPLOYEMENT_TYPE_PART_TIME, EMPLOYEMENT_TYPE_PART_TIME),
        (EMPLOYEMENT_TYPE_FREELANCING, EMPLOYEMENT_TYPE_FREELANCING),
        (EMPLOYEMENT_TYPE_CONTRACT, EMPLOYEMENT_TYPE_CONTRACT),
    )

    INDIA = 'India'

    COUNTRY_CHOICES = (
        (INDIA, INDIA),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=100, blank=True, null=True)
    job_title = models.CharField(max_length=100)
    role = models.CharField(max_length=100, blank=True)
    skills = models.ManyToManyField(Skill, related_name='jobs', blank=True)
    job_description = HTMLField() 
    experience = models.CharField(max_length=50)
    salary = models.CharField(max_length=50, blank=True, null=True)
    no_of_openings = models.PositiveSmallIntegerField()
    industry = models.CharField(max_length=100)
    functional_area = models.CharField(max_length=100)
    employement_type = models.CharField(max_length=50, 
                                        choices=EMPLOYEMENT_TYPE_CHOICES, 
                                        default=EMPLOYEMENT_TYPE_FULL_TIME
                                        )
    country = models.CharField(max_length=50, choices=COUNTRY_CHOICES)
    place = models.CharField(max_length=50, blank=True)
    visit_count = models.PositiveIntegerField(default=0)
    job_applied_count = models.PositiveIntegerField(default=0)

    publish = models.BooleanField(default=False)
    recommended_job = models.BooleanField(default=False)
    # dates
    uploaded_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    
    objects = JobManager()

    class Meta:
        verbose_name = 'Job Post'
        verbose_name_plural = 'Job Posts'
        ordering = ['-id']

    def save(self, *args, **kwargs):
        if self.slug:
            if slugify(self.job_title) != self.slug:
                self.slug = generate_unique_slug(Job, self.job_title, self)
        else: 
            self.slug = generate_unique_slug(Job, self.job_title)
        super(Job, self).save(*args, **kwargs)

    def __str__(self):
        return self.job_title
    
    @property
    def get_company_name(self):
        return Employer.objects.filter(user=self.user).first().company_name
    
    @property
    def get_all_skills(self):
        return self.skills.all()
    
    @property
    def get_salary(self):
        return f"{self.salary} INR per Month"
    