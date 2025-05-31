import logging
from datetime import datetime, timedelta

from django.contrib import messages
from django.db import transaction, IntegrityError
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from agphr.utils.decorators import allow_access_to

from users.models import User
from job.models import Skill, Job
from job.forms import AddSkill, CreateJobForm
from applicant.models import Applicant, WorkflowLog
from employer.models import Employer
from quiz.models import Quiz, Question, Option, Attempt

from .forms import (
    IndustryForm,
    FunctionalAreaForm,
    RoleForm,
    UserForm,
    ApplicantForm,
    QuizForm,
)
from .models import Industry, FunctionalArea, Role

@allow_access_to([User.SUPER_ADMIN])
def super_admin_analytics_view(request):
  return render(request, 'dashboard/super_admin/super_admin_analytics.html')

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
    applicants = Applicant.objects.all().order_by('-created_at')
    return render(request, 'dilip_dashboard_v2/super_admin/super_admin_applicant_list.html', {'applicants': applicants})

@allow_access_to([User.SUPER_ADMIN])
def super_admin_applicant_detail_view(request, pk):
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
    
    return render(request, 'dilip_dashboard_v2/super_admin/super_admin_applicant_detail.html', context)


    
@method_decorator(allow_access_to([User.SUPER_ADMIN]), name="dispatch")
class SuperAdminJobListView(ListView):
    template_name = 'dilip_dashboard_v2/super_admin/super_admin_job_list.html'
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

@allow_access_to([User.SUPER_ADMIN])
def super_admin_employer_list_view(request):
    employers = Employer.objects.all().order_by('-created_at')
    context = {
        'employers': employers,
    }
    return render(request, 'dilip_dashboard_v2/super_admin/super_admin_employer_list.html', context=context)

@allow_access_to([User.SUPER_ADMIN])
def super_admin_employer_detail_view(request, pk):
    employer = get_object_or_404(Employer, pk=pk)
    context = {
        'employer': employer,
    }
    return render(request, 'dashboard/super_admin/super_admin_employer_detail.html', context)

@allow_access_to([User.SUPER_ADMIN])
def super_admin_user_list_view(request):
    users = User.objects.all().order_by('-id')
    context = {
        'users': users,
    }
    return render(request, 'dashboard/super_admin/super_admin_user_list.html', context)

allow_access_to([User.SUPER_ADMIN])
def super_admin_create_industry_view(request):
    if request.method == "POST":
        form = IndustryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Industry created successfully')
            return redirect('super_admin:super_admin_create_industry')
        else:
            return render(request, 'dashboard/super_admin/super_admin_create_industry.html', {'form': form})
    else:
        form = IndustryForm()
    return render(request, 'dashboard/super_admin/super_admin_create_industry.html', {'form': form})

allow_access_to([User.SUPER_ADMIN])
def super_admin_create_functional_area_view(request):
    if request.method == 'POST':
        form = FunctionalAreaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Functional area created successfully!')
            return redirect('super_admin:super_admin_create_functional_area')
    else:
        form = FunctionalAreaForm()
    return render(request, 'dashboard/super_admin/super_admin_create_functional_area.html', {'form': form})

allow_access_to([User.SUPER_ADMIN])
def super_admin_create_role_view(request):
    if request.method == 'POST':
        form = RoleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Role created successfully!')
            return redirect('super_admin:super_admin_create_role')
    else:
        form = RoleForm() 
    return render(request, 'dashboard/super_admin/super_admin_create_role.html', {'form': form})

allow_access_to([User.SUPER_ADMIN])
def super_admin_industry_list_view(request):
    industries = Industry.objects.all()
    return render(request, 'dashboard/super_admin/super_admin_industry_list.html', {'industries': industries})

allow_access_to([User.SUPER_ADMIN])
def super_admin_functional_area_list_view(request):
    functional_areas = FunctionalArea.objects.all()
    return render(request, 'dashboard/super_admin/super_admin_functional_area_list.html', {'functional_areas': functional_areas})

allow_access_to([User.SUPER_ADMIN])
def super_admin_role_list_view(request):
    roles = Role.objects.all()
    return render(request, 'dashboard/super_admin/super_admin_role_list.html', {'roles': roles})

allow_access_to([User.SUPER_ADMIN])
def super_admin_update_industry_view(request, pk):
    industry = get_object_or_404(Industry, pk=pk)
    if request.method == 'POST':
        form = IndustryForm(request.POST, instance=industry)
        if form.is_valid():
            form.save()
            messages.success(request, 'Industry updated successfully!')
            return redirect('super_admin:super_admin_update_industry', pk=pk)  # Redirect to the list view
    else:
        form = IndustryForm(instance=industry)
    return render(request, 'dashboard/super_admin/super_admin_update_industry.html', {'form': form, 'industry': industry})

allow_access_to([User.SUPER_ADMIN])
def super_admin_update_functional_area_view(request, pk):
    functional_area = get_object_or_404(FunctionalArea, pk=pk)
    industries = Industry.objects.all()
    functional_areas = FunctionalArea.objects.all()
    roles = Role.objects.all()

    if request.method == 'POST':
        form = FunctionalAreaForm(request.POST, instance=functional_area)
        if form.is_valid():
            form.save()
            messages.success(request, 'Functional area updated successfully!')
            return redirect('super_admin:super_admin_update_functional_area', pk=pk)
    else:
        form = FunctionalAreaForm(instance=functional_area)
        context = {
            'form': form, 
            'functional_area': functional_area,
            'industries': industries,
            'functional_areas': functional_areas,
            'roles': roles
            }
    return render(request, 'dashboard/super_admin/super_admin_update_functional_area.html', context)

allow_access_to([User.SUPER_ADMIN])
def super_admin_update_role_view(request, pk):
    role = get_object_or_404(Role, pk=pk)
    if request.method == 'POST':
        form = RoleForm(request.POST, instance=role)
        if form.is_valid():
            form.save()
            messages.success(request, 'Role updated successfully!')
            return redirect('super_admin:super_admin_update_role', pk=pk)
    else:
        form = RoleForm(instance=role)
    return render(request, 'dashboard/super_admin/super_admin_update_role.html', {'form': form, 'role': role})

# AJAX views for dependent dropdowns
from django.http import JsonResponse
def get_functional_areas(request):
    industry_id = request.GET.get("industry_id")
    functional_areas = FunctionalArea.objects.filter(industry_id=industry_id)
    data = [{"id": fa.id, "name": fa.name} for fa in functional_areas]
    return JsonResponse(data, safe=False)

def get_roles(request):
    functional_area_id = request.GET.get("functional_area_id")
    roles = Role.objects.filter(functional_area_id=functional_area_id)
    data = [{"id": role.id, "name": role.name} for role in roles]
    return JsonResponse(data, safe=False)

@allow_access_to([User.SUPER_ADMIN])
def super_admin_add_resume_view(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        applicant_form = ApplicantForm(request.POST, request.FILES)
        
        if user_form.is_valid() and applicant_form.is_valid():
            user = user_form.save()

            applicant = applicant_form.save(commit=False)
            
            applicant.user = user
            applicant.applicant_type = Applicant.ApplicantType.WALKIN
            
            selected_industry = applicant_form.cleaned_data['industry']
            
            applicant.extra_fields['category'] = selected_industry.name
            applicant.save()
            messages.success(request, "Profile created and resume uploaded successfully.")
            WorkflowLog.objects.create(
                user=user,
                updated_by=request.user
            )
            return redirect(".")
        else:
            context = {
                "user_form": user_form,
                "applicant_form": applicant_form,
            }
            messages.error(request, "An error occurred while submitting the form.")
            return render(request, 'dashboard/super_admin/super_admin_add_resume.html', context)
    else:
        user_form = UserForm()
        applicant_form = ApplicantForm()
        industries = Industry.objects.all()
        
        context = {
            "user_form": user_form,
            "applicant_form": applicant_form,
            "industries": industries
        }
        return render(request, 'dashboard/super_admin/super_admin_add_resume.html', context)


@allow_access_to([User.SUPER_ADMIN])
def super_admin_resume_list_view(request):
    applicants = Applicant.objects.filter(applicant_type=Applicant.ApplicantType.WALKIN).order_by('-created_at')
    return render(request, 'dilip_dashboard_v2/super_admin/super_admin_resume_list.html', {'applicants': applicants})


@allow_access_to([User.SUPER_ADMIN])
def super_admin_create_question_view(request):
    if request.method == 'POST':
        quiz_id = request.POST.get('quiz')
        try:
            quiz = Quiz.objects.get(id=quiz_id)  
            
            question_types = request.POST.getlist('question_type[]')
            contents = request.POST.getlist('content[]')
            points = request.POST.getlist('points[]')

            if not (len(question_types) == len(contents) == len(points)):
                raise ValueError("Mismatched data lengths for questions.")

            with transaction.atomic():
                for idx, content in enumerate(contents):
                    question_type = question_types[idx]
                    point = points[idx]
                    
                    if not content or not point.isdigit():
                        raise ValueError(f"Invalid content or points for question {idx+1}")

                    question = Question.objects.create(
                        quiz=quiz,
                        content=content,
                        question_type=question_type,
                        points=int(point)
                    )

                    if question_type == 'mcq':
                        options = request.POST.getlist(f'options[{idx+1}][]')  # Get all options for the question
                        correct_flags = request.POST.getlist(f'is_correct[{idx+1}][]')  # Get the correct flags

                        if not options:
                            raise ValueError(f"At least one option must be provided for question {idx+1}.")
                        if not correct_flags:
                            raise ValueError(f"At least one option must be marked as correct for question {idx+1}.")
                        
                        for option_idx, option_text in enumerate(options):
                            if option_text:  # Ensure options aren't empty
                                # Check if the current option is marked as correct
                                is_correct = correct_flags[option_idx] == "on" if option_idx < len(correct_flags) else False
                                Option.objects.create(
                                    question=question,
                                    text=option_text,
                                    is_correct=is_correct
                                )

            messages.success(request, 'Questions added successfully!')
            return redirect('super_admin:super_admin_question_list')

        except Quiz.DoesNotExist:
            messages.error(request, 'Quiz not found.')
        except IntegrityError:
            messages.error(request, 'An error occurred while saving the questions. Please try again.')
        except ValueError as ve:
            messages.error(request, str(ve))
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {e}")

    quizzes = Quiz.objects.all()
    return render(request, 'dilip_dashboard_v2/super_admin/quiz/super_admin_create_question.html', {'quizzes': quizzes})

@allow_access_to([User.SUPER_ADMIN])
def super_admin_update_question_view(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    options = Option.objects.filter(question=question)
    quizzes = Quiz.objects.all()

    if request.method == 'POST':
        question_type = request.POST.get('question_type')
        content = request.POST.get('content')
        points = request.POST.get('points')
        quiz_id = request.POST.get('quiz')
        quiz = get_object_or_404(Quiz, id=quiz_id)

        # Update question fields
        question.question_type = question_type
        question.content = content
        question.points = points
        question.quiz = quiz
        question.save()

        # Log the POST data for debugging
        print("POST data:", request.POST)

        # Clear old options
        Option.objects.filter(question=question).delete()

        # Get options and checkbox states from POST data
        options_list = request.POST.getlist('options[]')
        for index, text in enumerate(options_list):
            checkbox_name = f'is_correct_{index}'
            is_correct = request.POST.get(checkbox_name) == 'on'

            if text.strip():  # Ensure no empty options are saved
                Option.objects.create(
                    question=question,
                    text=text.strip(),
                    is_correct=is_correct
                )

        messages.success(request, 'Question updated successfully.')
        return redirect('super_admin:super_admin_question_list')

    return render(request, 'dilip_dashboard_v2/super_admin/quiz/super_admin_update_question.html', {
        'question': question,
        'options': options,
        'quizzes': quizzes,
    })

@allow_access_to([User.SUPER_ADMIN])
def super_admin_delete_question_view(request, question_id):
    question = get_object_or_404(Question, id=question_id)

    if request.method == 'POST':
        question.delete()

        messages.success(request, 'Question deleted successfully.')

        return redirect('super_admin:super_admin_question_list')
    
@allow_access_to([User.SUPER_ADMIN])
def super_admin_delete_question_choice_view(request, choice_id):
    choice = Option.objects.get(id=choice_id)
    choice.delete()
    messages.success(request, "Choice deleted successfully")
    return redirect(".")

@allow_access_to([User.SUPER_ADMIN])
def super_admin_question_list_view(request):
    questions = Question.objects.all().order_by("-id")
    quizes = Quiz.objects.all().prefetch_related('questions')

    return render(request, 'dilip_dashboard_v2/super_admin/quiz/super_admin_question_list.html', {
        'questions': questions,
        'quizes': quizes,
    })

@allow_access_to([User.SUPER_ADMIN])
def super_admin_quiz_result_list_view(request):
    quizes = Quiz.objects.all().prefetch_related('questions')  # Fetch related questions for each quiz efficiently
    return render(request, 'dilip_dashboard_v2/super_admin/quiz/super_admin_quiz_result_list.html', {
        'quizes': quizes,
    })

@allow_access_to([User.SUPER_ADMIN])
def super_admin_quiz_attended_list_view(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    selected_date_str = request.GET.get('date')
    today = timezone.localdate()
    if selected_date_str:
        try:
            selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, "Invalid date format. Use YYYY-MM-DD.")
            selected_date = today
    else:
        selected_date = today

    # Get initial attempt queryset
    attempts_qs = Attempt.objects.filter(quiz=quiz, completed_at__date=selected_date)

    # If no data for selected date, fallback to latest available date with attempts
    if not attempts_qs.exists() and not selected_date_str:
        latest_attempt = (
            Attempt.objects.filter(quiz=quiz)
            .annotate(date=TruncDate('completed_at'))
            .order_by('-date')
            .values_list('date', flat=True)
            .first()
        )
        if latest_attempt:
            selected_date = latest_attempt
            attempts_qs = Attempt.objects.filter(quiz=quiz, completed_at__date=selected_date)
        else:
            messages.info(request, "No attempts found for this quiz.")

    # Get all available dates with attempt counts
    attempts_by_date = (
        Attempt.objects.filter(quiz=quiz)
        .annotate(date=TruncDate('completed_at'))
        .values('date')
        .annotate(count=Count('id'))
        .order_by('-date')
    )
    
    return render(request, 'dilip_dashboard_v2/super_admin/quiz/super_admin_quiz_attended_list.html', {
        'quiz': quiz,
        'attempts': attempts_qs.select_related('user'),
        'attempts_by_date': attempts_by_date,
        'selected_date': selected_date,
        'today': today,
    })

@allow_access_to([User.SUPER_ADMIN])
def super_admin_quiz_list(request):
    quizzes = Quiz.objects.filter(created_by=request.user)
    return render(request, 'quiz/super_admin_quiz_list.html', {'quizzes': quizzes})

@allow_access_to([User.SUPER_ADMIN])
def super_admin_create_quiz(request):
    if request.method == 'POST':
        form = QuizForm(request.POST)
        
        # Handling validation for required fields manually
        title = request.POST.get('title')
        description = request.POST.get('description')
        duration = request.POST.get('duration')

        # Basic validation for required fields
        if not title or not description or not duration:
            messages.error(request, "All fields are required.")
            return render(request, 'quiz/super_admin_create_quiz.html', {'form': form})

        try:
            # Try to convert duration into minutes
            duration_minutes = int(duration) if duration else 0
            duration_obj = timedelta(minutes=duration_minutes) if duration_minutes else None
        except ValueError:
            duration_obj = None

        # Check if quiz with the same title already exists
        if Quiz.objects.filter(title=title).exists():
            messages.error(request, "Quiz with this title already exists.")
            return render(request, 'quiz/super_admin_create_quiz.html', {'form': form})

        # Create the quiz object
        quiz = Quiz.objects.create(
            title=title,
            description=description,
            created_by=request.user,
            is_timed=True if duration_obj else False,
            duration=duration_obj
        )
        messages.success(request, "Quiz created successfully!")
        return redirect('super_admin:super_admin_question_list')

    else:
        form = QuizForm()  # Show an empty form for GET request

    return render(request, 'quiz/super_admin_create_quiz.html', {'form': form})

@allow_access_to([User.SUPER_ADMIN])
def super_admin_edit_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, created_by=request.user)

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        duration = request.POST.get('duration')

        errors = {}

        if not title:
            errors['title'] = "This field is required."
        if not duration:
            errors['duration'] = "This field is required."

        if Quiz.objects.exclude(id=quiz.id).filter(title=title, created_by=request.user).exists():
            messages.error(request, "Another quiz with this title already exists.")
            return render(request, 'quiz/super_admin_edit_quiz.html', {
                'quiz': quiz,
                'title': title,
                'description': description,
                'duration': duration,
                'errors': errors
            })

        if errors:
            return render(request, 'quiz/super_admin_edit_quiz.html', {
                'quiz': quiz,
                'title': title,
                'description': description,
                'duration': duration,
                'errors': errors
            })

        try:
            duration_minutes = int(duration)
            quiz.duration = timedelta(minutes=duration_minutes)
            quiz.is_timed = True
        except ValueError:
            quiz.duration = None
            quiz.is_timed = False

        quiz.title = title
        quiz.description = description
        quiz.save()
        messages.success(request, "Quiz updated successfully!")
        return redirect('super_admin:super_admin_question_list')

    return render(request, 'quiz/super_admin_edit_quiz.html', {'quiz': quiz})

@allow_access_to([User.SUPER_ADMIN])
def super_admin_delete_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, created_by=request.user)
    if request.method == 'POST':
        quiz.delete()
        messages.success(request, "Quiz deleted successfully!")
        return redirect('super_admin:super_admin_question_list')
    return render(request, 'quiz/super_admin_delete_quiz.html', {'quiz': quiz})

