from django.contrib import admin
from .models import Applicant, Application

admin.site.register((Applicant, Application))
