from django.urls import path
from .views import (
    applicant_list_view, 
    add_applicant_view,
    applicant_detail_view,
    update_applicant_view
)

app_name="application_handler"
urlpatterns = [
    path("applicant-list/", applicant_list_view, name="applicant_list"),
    path("add-applicant/", add_applicant_view, name="add_applicant"),
    path("update-applicant/<int:pk>/", update_applicant_view, name="update_applicant"),
    path('applicant-detail/<int:pk>/', applicant_detail_view, name='applicant_detail'),
]
