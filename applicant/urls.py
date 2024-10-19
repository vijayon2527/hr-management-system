from django.urls import path
from . views import (applicant_dashboard_view,
                    applicant_personal_profile_view,
                    applicant_professional_profile_view,
                    applicant_resume_view,
                    applied_job_view,
                    applicant_change_password_view,
                    applicant_delete_account_view,
                    apply_job_view,

                    )

app_name='applicant'
urlpatterns=[
    path('applicant-dashboard/', applicant_dashboard_view, name='applicant_dashboard'),
    path('applicant-personal-profile/', applicant_personal_profile_view, name='applicant_personal_profile'),
    path('applicant-professional-profile/', applicant_professional_profile_view, name='applicant_professional_profile'),
    path('applicant-resume/', applicant_resume_view, name='applicant_resume'),
    path('applicant-applied-jobs/', applied_job_view, name='applied_job'),
    path('applicant-change-password/', applicant_change_password_view, name='applicant_change_password'),
    path('applicant-delete-account/', applicant_delete_account_view, name='applicant_delete_account'),
    path('applicant-apply-job/<str:slug>/', apply_job_view, name='apply_job'),
]