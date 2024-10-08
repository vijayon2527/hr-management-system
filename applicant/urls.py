from django.urls import path
from . views import (applicant_analytics_view,
                    applicant_profile_view,
                    applied_job_view,
                    apply_job_view
                    )

app_name='applicant'
urlpatterns=[
    path('applicant-profile/', applicant_profile_view, name='applicant_profile'),
    path('applicant-applied-jobs/', applied_job_view, name='applied_job'),
    path('applicant-apply-job/<str:slug>/', apply_job_view, name='apply_job'),
]