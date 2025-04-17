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
                    super_admin_toggle_recommended_jobs_view,

                    super_admin_employer_list_view,
                    super_admin_employer_detail_view,
                    super_admin_user_list_view,

                    super_admin_create_industry_view,
                    super_admin_create_functional_area_view,
                    super_admin_create_role_view,

                    super_admin_industry_list_view,
                    super_admin_functional_area_list_view,
                    super_admin_role_list_view,

                    super_admin_update_industry_view,
                    super_admin_update_functional_area_view,
                    super_admin_update_role_view,
                    get_functional_areas,
                    get_roles,

                    super_admin_add_resume_view,
                    super_admin_resume_list_view,
                    super_admin_applicant_detail_view,

                    super_admin_create_question_view,
                    super_admin_question_list_view,
                    super_admin_update_question_view,
                    super_admin_delete_question_choice_view,
                    super_admin_quiz_result_list_view,
                    super_admin_delete_question_view,
                    super_admin_quiz_attended_list_view,

                    super_admin_create_quiz,
                    super_admin_edit_quiz,
                    super_admin_delete_quiz,
                    super_admin_quiz_list,
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

    path("super_admin-employer-list/", super_admin_employer_list_view, name='super_admin_employer_list'),
    path("super_admin-employer-detail/<int:pk>/", super_admin_employer_detail_view, name='super_admin_employer_detail'),

    path("super_admin-user-list/", super_admin_user_list_view, name='super_admin_user_list'),
    
    path("super_admin-create-industry/", super_admin_create_industry_view, name='super_admin_create_industry'),
    path("super_admin-create-functional-area/", super_admin_create_functional_area_view, name='super_admin_create_functional_area'),
    path("super_admin-create-role/", super_admin_create_role_view, name='super_admin_create_role'),

    path("super_admin-industry-list/", super_admin_industry_list_view, name='super_admin_industry_list'),
    path("super_admin-functional-area-list/", super_admin_functional_area_list_view, name='super_admin_functional_area_list'),
    path("super_admin-role-list/", super_admin_role_list_view, name='super_admin_role_list'),

    path("super_admin-update-industry/<int:pk>/", super_admin_update_industry_view, name='super_admin_update_industry'),
    path("super_admin-update-functional-area/<int:pk>/", super_admin_update_functional_area_view, name='super_admin_update_functional_area'),
    path("super_admin-update-role/<int:pk>/", super_admin_update_role_view, name='super_admin_update_role'),

    path('get-functional-areas/', get_functional_areas, name='get_functional_areas'),
    path('get-roles/', get_roles, name='get_roles'),
    path('super_admin-add-resume/', super_admin_add_resume_view, name='add_resume'),
    path('super_admin-resume-list/', super_admin_resume_list_view, name='resume_list'),
    path('super_admin-applicant-detail/<int:pk>/', super_admin_applicant_detail_view, name='applicant_detail'),
    path('super_admin-create-question/', super_admin_create_question_view, name='super_admin_create_question'),
    path('super_admin-question-list/', super_admin_question_list_view, name='super_admin_question_list'),
    path('super_admin-update-question/<int:question_id>/', super_admin_update_question_view, name='super_admin_update_question'),
     path('question/<int:question_id>/delete/', super_admin_delete_question_view, name='super_admin_delete_question'),
    path('super_admin-delete-question-choice/<int:choice_id>/', super_admin_delete_question_choice_view, name='super_admin_delete_question_choice'),
    path('super_admin-quiz-list/', super_admin_quiz_result_list_view, name='super_admin_quiz_result_list'),
    path('super_admin-quiz-attended-list/<int:quiz_id>/', super_admin_quiz_attended_list_view, name='super_admin_quiz_attended_list'),
    path('quizzes/',super_admin_quiz_list , name='super_admin_quiz_list'),
    path('quizzes/create/',super_admin_create_quiz, name='super_admin_create_quiz'),
    path('<int:quiz_id>/edit/', super_admin_edit_quiz, name='super_admin_edit_quiz'),
    path('<int:quiz_id>/delete/',super_admin_delete_quiz, name='super_admin_delete_quiz'),

]
