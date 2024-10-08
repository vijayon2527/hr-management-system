from django.urls import path
from . import views
app_name='job'
urlpatterns=[
    path("", views.job_list, name='job_list'),
    path("search/", views.search, name='search'),
    path("skillSearch/", views.skillSearch, name='skillSearch'),
    path("search-result/", views.search_result, name='skillSearch'),
]