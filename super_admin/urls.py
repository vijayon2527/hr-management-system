from django.urls import path
from .views import (super_admin_analytics_view,
                    super_admin_skill_list_view,
                    super_admin_skill_detail_view,
                    super_admin_update_skill_view,
                    super_admin_delete_skill_view,
                    super_admin_create_skill_view,

                    super_admin_applicant_list_view,
                    super_admin_job_list_view,
                    super_admin_job_update_view,
                    super_admin_job_delete_view,
                    super_admin_job_publish_view,
                    super_admin_job_unpublish_view,
                    super_admin_job_detail_view,
                    super_admin_toggle_recommended_jobs_view
                    )

app_name='super_admin'
urlpatterns = [
    path('super-admin-analytics/', super_admin_analytics_view, name='super_admin_analytics'),
    path("super_admin-create-skill/", super_admin_create_skill_view, name='super_admin_create_skill'),
    path("super_admin-skill-list/", super_admin_skill_list_view, name='super_admin_skill_list'),
    path("super_admin-skill-detail/<int:pk>/", super_admin_skill_detail_view, name='super_admin_skill_detail'),
    path("super_admin-update-skill/<int:pk>/", super_admin_update_skill_view, name='super_admin_update_skill'),
    path("super_admin-delete-skill/<int:pk>/", super_admin_delete_skill_view, name='super_admin_delete_skill'),
 
    path("super_admin-applicant-list/", super_admin_applicant_list_view, name='super_admin_applicant_list'),
    
    path("super_admin-job-list/", super_admin_job_list_view, name='super_admin_job_list'),
    path("super_admin-job-detail/<slug>/", super_admin_job_detail_view, name='super_admin_job_detail'),
    path("super_admin-update-job/<slug>/", super_admin_job_update_view, name='super_admin_job_update'),
    path("super_admin-delete-job/<slug>/", super_admin_job_delete_view, name='super_admin_job_delete'),
    path("super_admin-publish-job/<slug>/", super_admin_job_publish_view, name='super_admin_job_publish'),
    path("super_admin-unpublish-job/<slug>/", super_admin_job_unpublish_view, name='super_admin_job_unpublish'),
    path("super_admin-toggle-recommended-jobs/<slug>/", super_admin_toggle_recommended_jobs_view, name='super_admin_toggle_recommended_jobs'),


]
