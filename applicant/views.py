from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse

from agphr.utils.decorators import allow_access_to
from users.models import User
from applicant.models import Applicant, Application
from job.models import Job
from .models import Job, Applicant, Application

from applicant.forms import (
    ApplicantProfileForm, 
    ApplicantUserProfileForm,
    ApplicantResumeForm
)
from common.forms import UserPasswordChangeForm
from common.utils import change_user_password

@allow_access_to([User.APPLICANT_USER])
def applicant_dashboard_view(request,):
  return render(request, 'dashboard/applicant/applicant_dashboard.html')

@allow_access_to([User.APPLICANT_USER])   
def applicant_personal_profile_view(request):
    user = request.user
    applicant, created = Applicant.objects.get_or_create(user=user)
    if request.method=="POST":
        form = ApplicantUserProfileForm(request.POST, request.FILES, instance=user)
        resume_form = ApplicantResumeForm(request.POST, request.FILES, instance=applicant)
        if form.is_valid() and resume_form.is_valid():
            form.save()
            resume_form.save()
            messages.success(request, "Profile updated successfully")
            return redirect("applicant:applicant_professional_profile")
        else:
            return render(request, 'dashboard/applicant/applicant_personal_profile.html', {'form': form, 'resume_form': resume_form})
    else:
        form = ApplicantUserProfileForm(instance=user)
        resume_form = ApplicantResumeForm(instance=applicant)
    return render(request, 'dashboard/applicant/applicant_personal_profile.html', {'form': form, 'resume_form': resume_form})

@allow_access_to([User.APPLICANT_USER])   
def applicant_profile_picture_view(request):
    if request.method=="POST":
        profile_pic = request.FILES.get('profile_picture')
        user = request.user
        user.profile_pic = profile_pic
        user.save()
        messages.success(request, "Profile Picture updated successfully")
        return redirect('applicant:applicant_personal_profile')

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


@csrf_exempt  # If you need to disable CSRF for testing; better to implement proper CSRF handling
def apply_job_view(request, slug):
    if not request.user.is_authenticated:
        messages.error(request, "Please login as applicant to apply for a job.")
        return JsonResponse({
            'success': False,
            'redirect_url': reverse('users:login'),  # Assuming 'login' is the name of your login view
            'message': "You need to be logged in to apply for a job."
        })

    job = get_object_or_404(Job, slug=slug)
    user = request.user

    if request.method == "POST":
        try:
            applicant = Applicant.objects.get(user=user)

            if not applicant.user.is_profile_completed:
                messages.error(request, "Please update your profile to apply for a job.")
                return JsonResponse({
                    'success': False,
                    'redirect_url': reverse('applicant:applicant_personal_profile'),
                    'message': "Please update your profile to apply for a job."
                })

            if Application.objects.filter(job=job, applicant=applicant).exists():
                return JsonResponse({
                    'success': False,
                    'message': "You have already applied for this job."
                })

            # Create application
            Application.objects.create(job=job, applicant=applicant)
            job.job_applied_count += 1
            job.save()

            return JsonResponse({
                'success': True,
                'message': "You have successfully applied for this job."
            })

        except Applicant.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': "You need to register as an applicant before applying for jobs."
            })

        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': "Something went wrong. Please try again later."
            })

    return JsonResponse({
        'success': False,
        'message': "Invalid request method."
    })