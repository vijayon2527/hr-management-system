from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from agphr.utils.decorators import allow_access_to
from django.db import transaction
from users.models import User
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from applicant.models import Applicant, Application
from applicant.forms import (ApplicantProfileForm, 
                             ApplicantUserProfileForm
							)
from job.models import Job
import logging

@allow_access_to([User.APPLICANT_USER])
def applicant_analytics_view(request,):
  return render(request, 'dashboard/applicant/applicant_analytics.html')

@allow_access_to([User.APPLICANT_USER])
def applied_job_view(request,):
  applications = Application.objects.filter(applicant__user=request.user)
  context = {
      'applications': applications
      }
  return render(request, 'dashboard/applicant/applied_job.html', context)

@allow_access_to([User.APPLICANT_USER])   
def applicant_profile_view(request):
    user = request.user
    applicant = Applicant.objects.filter(user=user).first()
    if request.method=="POST":
        applicant_user_form = ApplicantUserProfileForm(request.POST, request.FILES, instance=user)
        applicant_profile_form = ApplicantProfileForm(request.POST, request.FILES, instance=applicant)
        if applicant_user_form.is_valid() and applicant_profile_form.is_valid():
            applicant_user_form.save()
            applicant_profile_form = applicant_profile_form.save(commit=False)
            applicant_profile_form.user = request.user
            applicant_profile_form.save()
            messages.success(request, "Profile updated successfully")
            return redirect("applicant:applicant_profile")
        else:
             context = {
                 'applicant_user_form': applicant_user_form,
                 'applicant_profile_form': applicant_profile_form 
                 }
             return render(request, 'dashboard/applicant/applicant_profile.html', context)
    else:
        context = {
                 'applicant_user_form': ApplicantUserProfileForm(instance=user),
                 'applicant_profile_form': ApplicantProfileForm(instance=applicant) 
                 }
        return render(request, 'dashboard/applicant/applicant_profile.html', context)

@login_required 
def apply_job_view(request, slug):
    if request.method == "POST":
        job = get_object_or_404(Job, slug=slug)
        user = request.user

        try:
            applicant = Applicant.objects.get(user=user)
        except Applicant.DoesNotExist:
            messages.warning(request, "You need to register as an applicant before applying for jobs.")
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
