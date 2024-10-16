import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView

from hitcount.views import HitCountDetailView

from job.models import Job, Skill
from users.models import User


@csrf_exempt
def search(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == "GET":
        if 'term' in request.GET:
            term = request.GET.get("term")
            skill_queryset = Skill.objects.filter(Q(name__istartswith=term))
            job_queryset = Job.objects.filter(Q(job_title__istartswith=term))
    
            skill_query = [query.name for query in skill_queryset]
            job_query =[query.job_title for query in job_queryset]
            list_queryset = skill_query + job_query
        if 'location' in request.GET:
            location = request.GET.get("location")
            queryset = Job.objects.filter(Q(place__istartswith=location))
            list_queryset = [f'{query.place}, Karnataka' for query in queryset] 

        unique_list_queryset = list(dict.fromkeys(list_queryset))
        return JsonResponse(unique_list_queryset, safe=False)   

class HomeView(ListView):
    model = Job
    template_name = 'home.html'
    context_object_name = 'jobs'
    def get_queryset(self, *args, **kwargs):
        return Job.objects.recommended_jobs()

class JobList(ListView):
    model = Job
    template_name = 'job/job_list.html'
    context_object_name = 'jobs'
    paginate_by = 10
    
    def get_queryset(self):
        locations = self.request.GET.get('locations')
        skills = self.request.GET.get('skills')
        object_list = Job.objects.published_job_lists()

        location_lists = []
        skill_lists = []

        if locations:
            location_lists = [location.strip() for location in locations.split(",") if location.strip()]

        if skills:
            skill_lists = [skill.strip() for skill in skills.split(",") if skill.strip()]

            search_skills = location_lists + skill_lists
            object_list = Job.objects.published_job_lists(search_skills)        
            job_length = len(object_list)
            if job_length < 1:
                object_list = Job.objects.published_job_lists()
                messages.warning(self.request, "No job found.")
            else:
                messages.success(self.request, f"{job_length} Job found.")
        return object_list
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        job_title = self.request.GET.get('job_title')
        if job_title:
            try:
                job = Job.objects.get(slug=job_title)
                context['job'] = job
            except Job.DoesNotExist:
                messages.warning(self.request, "The requested job was not found.")
                context['job'] = None
        else:
            job_list = context.get('jobs')
            if job_list:
                context['job'] = job_list[0]  # Set the first job as default
            else:
                context['job'] = None

        return context
    
    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            if 'job_title' in self.request.GET:  # If it's a request for job details
                job_detail_html = render_to_string('job/listing/partials/job_detail_card.html', {'job': context['job']})
                return JsonResponse({
                    'job_detail_html': job_detail_html
                })
            else:  # Otherwise, it's a request to load more jobs
                jobs_html = render_to_string('job/listing/partials/job_list_card.html', {'jobs': context['jobs']})
                return JsonResponse({
                    'jobs_html': jobs_html,
                    'has_next': context['page_obj'].has_next(),
                })
        
        return super().render_to_response(context, **response_kwargs)

job_list = JobList.as_view()

@csrf_exempt
def skillSearch(request):
    if request.method == "GET":
        if 'term' in request.GET:
            term = request.GET.get("term")
            list_queryset = Skill.objects.filter(name__icontains=term)
            skills_list = [{"id": skill.id, "label": skill.name} for skill in list_queryset]
            return JsonResponse(skills_list, safe=False)
        
def search_result(request):
    salary = request.GET.get("salary", None)
    freshness = request.GET.get("freshness", None)
    experience = request.GET.get("experience", None)
    country = request.GET.getlist("country", None)
    job_list = Job.objects.get_filtered_data(salary, freshness, experience, country)
    
    context = {'job_list':job_list,
               'freshness':freshness,
               'salary':salary,
               'experience':experience,
               }
    return render(request, 'job/search_result.html', context)