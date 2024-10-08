import logging
import xlwt

from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.db import transaction

from agphr.utils.decorators import allow_access_to
from job.models import Job
from job.forms import CreateJobForm
from applicant.models import Applicant, Application
from users.models import User

@allow_access_to([User.EMPLOYER])
def employer_analytics_view(request,):
  return render(request, 'dashboard/employer/employer_analytics.html')

def employer_profile_view(request):
    jobs = Job.objects.all()
    return render(request, 'dashboard/employer/employer_profile.html', {'jobs': jobs})

@method_decorator(allow_access_to([User.EMPLOYER]), name="dispatch")
class EmployerJobListView(ListView):
    template_name = 'dashboard/employer/employer_job_list.html'
    context_object_name = 'jobs'
    
    def get_queryset(self):
        query = self.request.GET.get('name')
        sorting_value = self.request.GET.get('sorting_value')
        user = self.request.user
        job = Job.objects.all_job_lists(query=query, sorting_value=sorting_value, user=user)
        
        if query is not None:
            job_length = len(job)
            messages.success(self.request, f"{job_length if job_length >= 1 else 'No'} job found for {query}.")
        
        return job
employer_job_list_view=EmployerJobListView.as_view()

@allow_access_to([User.EMPLOYER])
def employer_create_job_view(request):
    if request.method == "POST":
        form = CreateJobForm(request.POST)
        skill_ids = request.POST.getlist("skills")
        if form.is_valid():
            try:
                with transaction.atomic():
                    publish = form.cleaned_data.get('publish')
                    salary = form.cleaned_data.get('salary')
                    experience = form.cleaned_data.get('experience')
                    if not salary:
                        minimum_salary = request.POST.get('minimum_salary')
                        maximum_salary = request.POST.get('maximum_salary')
                        salary_measurement = request.POST.get('salary_measurement')
                        salary_currency = request.POST.get('salary_currency')
                        duration = request.POST.get('duration')
                        salary = f'{minimum_salary} to {maximum_salary} {salary_measurement} {salary_currency} {duration}'
                    if not experience:
                        minimum_experience_years = request.POST.get('minimum_experience_years')
                        maximum_experience_years = request.POST.get('maximum_experience_years')
                        experience = f'{minimum_experience_years} to {maximum_experience_years} Years'
                    user=request.user
                    form=form.save(commit=False)
                    form.user=user
                    form.salary=salary
                    form.experience=experience
                    if publish:
                        form.published_at=timezone.now()
                    form.save()
                    form.skills.set([int(id) for id in skill_ids])
                    messages.success(request, "Job uploaded successfully")
                    return redirect(".")
            except:
                logging.info("Not able to add the job")
                messages.warning(request, "Some error occured, please try again")
                return redirect(".")
        else:
            messages.warning(request, "No valid data")
    else:
        form = CreateJobForm()
    return render(request, 'dashboard/employer/employer_create_job.html', {'form': form})

@allow_access_to([User.EMPLOYER])
def employer_job_detail_view(request, slug):
    job = Job.objects.job_detail(slug)
    return render(request, 'dashboard/employer/employer_job_detail.html', {'job':job})

@allow_access_to([User.EMPLOYER])
def employer_job_update_view(request, slug):
    job = get_object_or_404(Job, slug=slug)
    if request.method == "POST":
        form = CreateJobForm(request.POST, instance=job)
        skill_ids = request.POST.getlist('skills')
        if form.is_valid():
            try:
                with transaction.atomic():
                    publish = form.cleaned_data.get('publish')
                    form=form.save(commit=False)
                    if publish:
                        form.published_at=timezone.now()
                    form.save()
                    form.skills.set([int(id) for id in skill_ids]) 
                    messages.success(request, "Job updated successfully")
                    return redirect("employer:employer_update_job", slug=job.slug)
            except:
                logging.info("Not able to update the job")
                messages.warning(request, "Not able to update, please try again")
                return redirect(".")
        else:
            messages.warning(request, "No valid data")
            return render(request, 'dashboard/employer/employer_job_update.html', {'form': form, 'job':job})

    else:
        form = CreateJobForm(instance=job)
    return render(request, 'dashboard/employer/employer_job_update.html', {'form': form, 'job':job})

allow_access_to([User.EMPLOYER])
def employer_job_delete_view(request, slug):
    job = get_object_or_404(Job, slug=slug)
    job.delete()
    messages.success(request, "Deleted successfully")
    return redirect(request.META.get('HTTP_REFERER'))

@allow_access_to([User.EMPLOYER])
def employer_job_publish_view(request, slug):
    job = get_object_or_404(Job, slug=slug)
    job.publish=True
    job.published_at=timezone.now()
    job.save()
    messages.success(request, "Published successfully")
    return redirect(request.META.get('HTTP_REFERER'))

@allow_access_to([User.EMPLOYER])
def employer_job_unpublish_view(request, slug):
    job = get_object_or_404(Job, slug=slug)
    job.publish=False
    job.published_at=None
    job.save()
    messages.success(request, "Unpublished successfully")
    return redirect(request.META.get('HTTP_REFERER'))

@method_decorator(allow_access_to([User.EMPLOYER]), name="dispatch")
class EmployerApplicantListView(ListView):
    model= Applicant
    template_name= 'dashboard/employer/employer_applicant_list.html'
    context_object_name = 'applicant_list'
    # paginate_by = 10
    def get_queryset(self, *args, **kwargs):
        query = self.request.GET.get('name')
        sorting_value = self.request.GET.get('sorting_value')
        applicant_list = Applicant.objects.all_applicant_lists(query, sorting_value)
        if query is not None:
            applicant_length = len(applicant_list)
            messages.success(self.request, f"{applicant_length if applicant_length >=1  else 'No'} applicant found.")
        return applicant_list
employer_applicant_list_view = EmployerApplicantListView.as_view()

@method_decorator(allow_access_to([User.EMPLOYER]), name="dispatch")
class EmployerApplicationListView(ListView):
    model= Application
    template_name= 'dashboard/employer/employer_application_list.html'
    context_object_name = 'application_list'
    # paginate_by = 10
    def get_queryset(self, *args, **kwargs):
        query = self.request.GET.get('name')
        sorting_value = self.request.GET.get('sorting_value')
        application_list = Application.objects.all_application_lists(query, sorting_value, employer=self.request.user)
        if query is not None:
            application_length = len(application_list)
            messages.success(self.request, f"{application_length if application_length >=1  else 'No'} application found.")
        return application_list
employer_application_list_view = EmployerApplicationListView.as_view()

@allow_access_to([User.EMPLOYER])
def employer_export_applicant_list_view(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="applicants.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Applicants')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ('Name', 
               'Mobile', 
               'Email Address', 
               'Notice period', 
               'LinkedIn link', 
               'Qualitative skills', 
               'Subject', 
               'message'
    )
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    font_style = xlwt.XFStyle()
    rows = Applicant.objects.values_list('user__name', 
                                            'user__mobile', 
                                            'user__email', 
                                            'notice_period', 
                                            'linkedin_link', 
                                            'qualitative_skills', 
                                            'subject', 
                                            'message'
                                            )
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    wb.save(response)
    return response

@allow_access_to([User.EMPLOYER])
def employer_toggle_recommended_jobs_view(request, slug):
    Job.objects.toggle_recommended_jobs(slug, user=request.user)
    messages.success(request, "action completed successfully")
    return redirect(request.META.get('HTTP_REFERER'))