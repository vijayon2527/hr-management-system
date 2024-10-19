from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from agphr.utils.decorators import allow_access_to
from users.models import User
from job.forms import  AddSkill
from job.models import Skill, Job
from job.forms import CreateJobForm
from applicant.models import Applicant
from employer.models import Employer
from django.utils import timezone
from django.db import transaction
import logging

@allow_access_to([User.SUPER_ADMIN])
def super_admin_analytics_view(request):
  return render(request, 'dashboard/super_admin/super_admin_analytics.html')

@allow_access_to([User.SUPER_ADMIN])
def super_admin_user_list_view(request):
    pass

@allow_access_to([User.SUPER_ADMIN])
def super_admin_user_detail_view(request, pk):
    pass

@allow_access_to([User.SUPER_ADMIN])
def super_admin_employeer_list_view(request):
    pass

@allow_access_to([User.SUPER_ADMIN])
def super_admin_employeer_detail_view(request, slug):
    pass

@allow_access_to([User.SUPER_ADMIN])
def super_admin_applicant_list_view(request):
    applicants = Applicant.objects.all()
    return render(request, 'dashboard/super_admin/super_admin_applicant_list.html', {'applicants': applicants})

@allow_access_to([User.SUPER_ADMIN])
def super_admin_applicant_detail_view(request):
    pass

@method_decorator(allow_access_to([User.SUPER_ADMIN]), name="dispatch")
class SuperAdminJobListView(ListView):
    template_name = 'dashboard/super_admin/super_admin_job_list.html'
    context_object_name = 'jobs'
    # paginate_by = 10
    
    def get_queryset(self):
        query = self.request.GET.get('name')
        sorting_value = self.request.GET.get('sorting_value')
        job = Job.objects.all_job_lists(query, sorting_value)
        if query is not None:
            job_length = len(job)
            messages.success(self.request, f"{job_length if job_length >=1  else 'No'} job found for {query}.")
        return job
super_admin_job_list_view=SuperAdminJobListView.as_view()

@allow_access_to([User.SUPER_ADMIN])
def super_admin_job_detail_view(request, slug):
    job = Job.objects.job_detail(slug)
    return render(request, 'dashboard/super_admin/super_admin_job_detail.html', {'job':job})

@allow_access_to([User.SUPER_ADMIN])
def super_admin_job_update_view(request, slug):
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
                    return redirect("super_admin:super_admin_job_update", slug=job.slug)
            except:
                logging.info("Not able to update the job")
                messages.error(request, "Not able to update, please try again")
                return redirect(".")
        else:
            messages.error(request, "No valid data")
            return render(request, 'dashboard/super_admin/super_admin_job_update.html', {'form': form, 'job':job})

    else:
        form = CreateJobForm(instance=job)
    return render(request, 'dashboard/super_admin/super_admin_job_update.html', {'form': form, 'job':job})

allow_access_to([User.SUPER_ADMIN])
def super_admin_job_delete_view(request, slug):
    job = get_object_or_404(Job, slug=slug)
    job.delete()
    messages.success(request, "Deleted successfully")
    return redirect(request.META.get('HTTP_REFERER'))

@allow_access_to([User.SUPER_ADMIN])
def super_admin_job_publish_view(request, slug):
    job = get_object_or_404(Job, slug=slug)
    job.publish=True
    job.published_at=timezone.now()
    job.save()
    messages.success(request, "Published successfully")
    return redirect(request.META.get('HTTP_REFERER'))

@allow_access_to([User.SUPER_ADMIN])
def super_admin_job_unpublish_view(request, slug):
    job = get_object_or_404(Job, slug=slug)
    job.publish=False
    job.published_at=None
    job.save()
    messages.success(request, "Unpublished successfully")
    return redirect(request.META.get('HTTP_REFERER'))

@allow_access_to([User.SUPER_ADMIN])
def super_admin_toggle_recommended_jobs_view(request, slug):
    Job.objects.toggle_recommended_jobs(slug)
    messages.success(request, "action completed successfully")
    return redirect(request.META.get('HTTP_REFERER'))

@allow_access_to([User.SUPER_ADMIN])
def super_admin_create_skill_view(request):
    pass

@allow_access_to([User.SUPER_ADMIN])
def super_admin_skill_list_view(request):
    pass

@allow_access_to([User.SUPER_ADMIN])
def super_admin_skill_detail_view(request, pk):
    pass

@allow_access_to([User.SUPER_ADMIN])
def super_admin_skill_update_view(request, pk):
    pass

@allow_access_to([User.SUPER_ADMIN])
def super_admin_skill_delete_view(request, pk):
    pass


@allow_access_to([User.SUPER_ADMIN])
def super_admin_create_skill_view(request):
    if request.method == "POST":
        form = AddSkill(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Skill added successfully")
    form = AddSkill()
    return render(request, 'dashboard/super_admin/super_admin_create_skill.html', {'form':form})

@method_decorator(allow_access_to([User.SUPER_ADMIN]), name="dispatch")
class SuperAdminSkillListView(ListView):
    model = Skill
    template_name = 'dashboard/super_admin/super_admin_skill_list.html'
    context_object_name = 'skills'
    
    def get_queryset(self, *args, **kwargs):
        query = self.request.GET.get('name')
        sorting_value = self.request.GET.get('sorting_value')
        skills = Skill.objects.skill_lists(query, sorting_value)
        if query is not None:
            skills_length = len(skills)
            messages.success(self.request, f"{skills_length if skills_length >=1  else 'No'} job found for {query}.")
        return skills
super_admin_skill_list_view = SuperAdminSkillListView.as_view()

@allow_access_to([User.SUPER_ADMIN])
def super_admin_skill_detail_view(request, pk):
    skill = Skill.objects.skill_detail(pk)
    return render(request, 'dashboard/super_admin/super_admin_skill_detail.html', {'skill':skill})

allow_access_to([User.SUPER_ADMIN])
def super_admin_update_skill_view(request, pk):
    skill = get_object_or_404(Skill, pk=pk)
    form = AddSkill(request.POST, instance=skill)
    if form.is_valid():
        form.save()
        messages.success(request, "Skill added successfully")

    form = AddSkill(instance=skill)
    return render(request, 'dashboard/super_admin/super_admin_update_skill.html', {'form':form})

@allow_access_to([User.SUPER_ADMIN])
def super_admin_delete_skill_view(request, pk):
    skill = Skill.objects.get(id=pk)
    skill.delete()
    messages.success(request, "Skill deleted successfully")
    return redirect('super_admin:super_admin_skill_list')

# @allow_access_to([User.SUPER_ADMIN])
def super_admin_employer_list_view(request):
    employers = Employer.objects.all()
    context = {
        'employers': employers,
    }
    return render(request, 'dashboard/super_admin/super_admin_employer_list.html', context=context)

@allow_access_to([User.SUPER_ADMIN])
def super_admin_employer_detail_view(request, pk):
    employer = get_object_or_404(Employer, pk=pk)
    context = {
        'employer': employer,
    }
    return render(request, 'dashboard/super_admin/super_admin_employer_detail.html', context)

@allow_access_to([User.SUPER_ADMIN])
def super_admin_user_list_view(request):
    users = User.objects.all()
    context = {
        'users': users,
    }
    return render(request, 'dashboard/super_admin/super_admin_user_list.html', context)