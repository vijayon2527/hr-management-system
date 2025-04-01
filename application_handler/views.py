from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from agphr.utils.decorators import allow_access_to
from users.models import User
from application_handler.forms import UserForm, ApplicantForm
from applicant.models import Applicant
from applicant.models import WorkflowLog
from super_admin.models import Industry
from .forms import *

@allow_access_to([User.APPLICATION_HANDLER])
def add_applicant_view(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        applicant_form = ApplicantForm(request.POST, request.FILES)

        if user_form.is_valid() and applicant_form.is_valid():
            try:
                with transaction.atomic():
                    user = user_form.save(commit=False)
                    fname = user_form.cleaned_data.get("first_name", "")[:1]
                    lname = user_form.cleaned_data.get("last_name", "")[:1]
                    mobile = user_form.cleaned_data.get("mobile", "")[:1]
                    raw_password = f"{fname}{lname}{mobile}@agphr".casefold()

                    user.set_password(raw_password)
                    user.save()

                    applicant = applicant_form.save(commit=False)
                    applicant.user = user
                    applicant.applicant_type = Applicant.ApplicantType.WALKIN

                    # Set industry as extra field
                    selected_industry = applicant_form.cleaned_data.get('industry')
                    if selected_industry:
                        if not isinstance(applicant.extra_fields, dict):
                            applicant.extra_fields = {}
                        applicant.extra_fields['category'] = selected_industry.name
                        applicant.extra_fields['created_by'] = request.user.id
                    
                    applicant.save()

                    applicant_form.save_m2m()

                    # Create Workflow Log
                    WorkflowLog.objects.create(
                        user=user,
                        updated_by=request.user
                    )

                messages.success(request, "Profile created and resume uploaded successfully.")
                return redirect(".")

            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")
                return redirect(".")

        else:
            messages.error(request, "An error occurred while submitting the form.")

    else:
        user_form = UserForm()
        applicant_form = ApplicantForm()

    industries = Industry.objects.all()
    context = {
        "user_form": user_form,
        "applicant_form": applicant_form,
        "industries": industries
    }
    return render(request, 'dilip_dashboard_v2/application_handler/add_applicant.html', context)

@allow_access_to([User.APPLICATION_HANDLER])
def update_applicant_view(request, pk):
    applicant = get_object_or_404(Applicant, id=pk)
    user = applicant.user
    
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        applicant_form = ApplicantForm(request.POST, request.FILES, instance=applicant)

        if user_form.is_valid() and applicant_form.is_valid():
            try:
                with transaction.atomic():
                    user = user_form.save()
                    
                    applicant = applicant_form.save(commit=False)
                    
                    # Update industry in extra fields
                    selected_industry = applicant_form.cleaned_data.get('industry')
                    if selected_industry:
                        if not isinstance(applicant.extra_fields, dict):
                            applicant.extra_fields = {}
                        applicant.extra_fields['category'] = selected_industry.name
                        applicant.extra_fields['updated_by'] = request.user.id
                    
                    applicant.save()
                    applicant_form.save_m2m()
                    
                    # Log the update
                    WorkflowLog.objects.create(
                        user=user,
                        updated_by=request.user
                    )
                    
                messages.success(request, "Profile updated successfully.")
                return redirect(".")

            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")
                return redirect(".")
        else:
            messages.error(request, "An error occurred while submitting the form.")
    else:
        user_form = UserForm(instance=user)
        applicant_form = ApplicantForm(instance=applicant)
    
    industries = Industry.objects.all()
    context = {
        "user_form": user_form,
        "applicant_form": applicant_form,
        "industries": industries
    }
    return render(request, 'dilip_dashboard_v2/application_handler/update_applicant.html', context)


@allow_access_to([User.APPLICATION_HANDLER])
def applicant_list_view(request):
    applicants = Applicant.objects.filter(applicant_type=Applicant.ApplicantType.WALKIN).order_by('-created_at')
    return render(request, 'dilip_dashboard_v2/application_handler/applicant_list.html', {'applicants': applicants})

@allow_access_to([User.APPLICATION_HANDLER])
def applicant_detail_view(request, pk):
    applicant = get_object_or_404(Applicant, id=pk)
    user = applicant.user

    # # Check if there's already an UNDER_REVIEW log, if not create one
    # existing_workflow = WorkflowLog.objects.filter(
    #     user=user, 
    #     status=WorkflowLog.WorkflowStatus.UNDER_REVIEW
    #     ).first()
    # if not existing_workflow:
    #     WorkflowLog.objects.create(
    #         user=user,
    #         updated_by=request.user,
    #         status=WorkflowLog.WorkflowStatus.UNDER_REVIEW
    #     )

    # Fetch all workflow logs for the user
    workflows = WorkflowLog.objects.filter(user=user).order_by("-timestamp")

    context = {
        "applicant": applicant,
        "workflows": workflows
    }
    
    return render(request, 'dilip_dashboard_v2/application_handler/applicant_detail.html', context)
