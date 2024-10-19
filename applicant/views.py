from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from agphr.utils.decorators import allow_access_to
from users.models import User
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from applicant.models import Applicant, Application
from applicant.forms import (ApplicantProfileForm, 
                             ApplicantUserProfileForm,
                             ApplicantResumeForm
							)
from common.forms import UserPasswordChangeForm
from common.utils import change_user_password
from job.models import Job

@allow_access_to([User.APPLICANT_USER])
def applicant_dashboard_view(request,):
  return render(request, 'dashboard/applicant/applicant_dashboard.html')

@allow_access_to([User.APPLICANT_USER])   
def applicant_personal_profile_view(request):
    user = request.user
    applicant, created = Applicant.objects.get_or_create(user=user)
    if request.method=="POST":
        form = ApplicantUserProfileForm(request.POST, instance=user)
        resume_form = ApplicantResumeForm(request.POST, request.FILES, instance=applicant)
        if form.is_valid() and resume_form.is_valid():
            form.save()
            resume_form.save()
            messages.success(request, "Profile updated successfully")
            return redirect("applicant:applicant_personal_profile")
        else:
            return render(request, 'dashboard/applicant/applicant_personal_profile.html', {'form': form, 'resume_form': resume_form})
    else:
        form = ApplicantUserProfileForm(instance=user)
        resume_form = ApplicantResumeForm(instance=applicant)
    return render(request, 'dashboard/applicant/applicant_personal_profile.html', {'form': form, 'resume_form': resume_form})

@allow_access_to([User.APPLICANT_USER])   
def applicant_professional_profile_view(request):
    user = request.user
    applicant, created = Applicant.objects.get_or_create(user=user)
    if request.method=="POST":
        form = ApplicantProfileForm(request.POST, instance=applicant)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully")
            return redirect("applicant:applicant_professional_profile")
        else:
            return render(request, 'dashboard/applicant/applicant_professional_profile.html', {'form': form})
    else:
        form = ApplicantProfileForm(instance=applicant)
    return render(request, 'dashboard/applicant/applicant_professional_profile.html', {'form': form})

@allow_access_to([User.APPLICANT_USER])
def applicant_resume_view(request,):
    user = request.user
    applicant = get_object_or_404(Applicant, user=user)
    if request.method=="POST":
        form = ApplicantResumeForm(request.POST, request.FILES, instance=applicant)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your resume has been updated successfully!')
            return redirect('applicant:applicant_resume')
        else:
            return render(request, 'dashboard/applicant/applicant_resume.html', {'form': form})
    else:   
        form = ApplicantResumeForm(instance=applicant)
    return render(request, 'dashboard/applicant/applicant_resume.html', {'form': form})

@allow_access_to([User.APPLICANT_USER])
def applied_job_view(request,):
  applications = Application.objects.filter(applicant__user=request.user)
  context = {
      'applications': applications
      }
  return render(request, 'dashboard/applicant/applied_job.html', context)

@allow_access_to([User.APPLICANT_USER])
def applicant_change_password_view(request,):
    if request.method == 'POST':
        form = UserPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password1']
            if change_user_password(request, request.user, old_password, new_password):
                return redirect('applicant:applicant_change_password')
        else:
            return render(request, 'dashboard/applicant/applicant_change_password.html',{'form': form})
    else:
        form = UserPasswordChangeForm(request.user)
    return render(request, 'dashboard/applicant/applicant_change_password.html',{'form': form})

@allow_access_to([User.APPLICANT_USER])
def applicant_delete_account_view(request):
    user = User.objects.get(id=request.user.id)
    user.delete()
    messages.success(request, 'Your account has been deleted successfully')
    return redirect('job:job_list')

@login_required 
def apply_job_view(request, slug):
    if request.method == "POST":
        job = get_object_or_404(Job, slug=slug)
        user = request.user

        try:
            applicant = Applicant.objects.get(user=user)
        except Applicant.DoesNotExist:
            messages.warning(request, "You need to register as an applicant before applying for jobs, or ipdate your applicant profile")
            return redirect(request.META.get('HTTP_REFERER', 'job:job_list'))

        if Application.objects.filter(job=job, applicant=applicant).exists():
            messages.warning(request, "You have already applied for this job.")
            return redirect(request.META.get('HTTP_REFERER', 'job:job_list')) 

        try:
            Application.objects.create(
                job=job,
                applicant=applicant,
            )
            messages.success(request, "You have successfully applied for this job.")
            return redirect(request.META.get('HTTP_REFERER', 'job:job_list'))

        except IntegrityError:
            messages.warning(request, "It looks like you've already applied for this job. Please check your application status.")
            return redirect(request.META.get('HTTP_REFERER', 'job:job_list'))

        except ValidationError as ve:
            messages.warning(request, "There was a problem with your submission. Please ensure all fields are filled out correctly.")
            return redirect(request.META.get('HTTP_REFERER', 'job:job_list'))

        except Exception as e:
            messages.warning(request, "Something went wrong. Please try again later.")
            return redirect(request.META.get('HTTP_REFERER', 'job:job_list'))

    # If the request is not POST, redirect to job list
    return redirect("job:job_list")
