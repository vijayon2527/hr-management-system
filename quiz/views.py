from django.shortcuts import render,redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from quiz.models import Quiz, Question, Attempt, Answer, Option
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from .forms import QuizForm
from datetime import timedelta
from django.contrib import messages


def answer_question_view(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.prefetch_related('options').all()

    quiz_duration = quiz.duration
    user_attempt, created = Attempt.objects.get_or_create(user=request.user, quiz=quiz)

    if not created and user_attempt.completed_at:
        return render(request, 'quiz/already_submitted.html')

    if created:
        user_attempt.started_at = now()
        user_attempt.save()
    
    elapsed_time = now() - user_attempt.started_at
    time_remaining = quiz_duration - elapsed_time

    
    if time_remaining.total_seconds() <= 0:
        # Auto-submit the quiz
        existing_answers = Answer.objects.filter(attempt=user_attempt).values_list('question_id', flat=True)
        result = {'total': len(questions), 'correct': 0, 'incorrect': 0, 'unanswered': 0}

        for question in questions:
            if question.id in existing_answers:
                continue  # Skip already answered
            # Mark unanswered
            result['unanswered'] += 1

        # Count correct/incorrect from existing answers
        for answer in Answer.objects.filter(attempt=user_attempt):
            if answer.selected_option.is_correct:
                result['correct'] += 1
            else:
                result['incorrect'] += 1

        user_attempt.score = result['correct']
        user_attempt.completed_at = now()
        user_attempt.save()

        return render(request, 'quiz/time_expired.html')  # Show that quiz has been auto-submitted

    if request.method == 'POST':
        submitted_data = request.POST
        result = {'total': len(questions), 'correct': 0, 'incorrect': 0, 'unanswered': 0}

        for question in questions:
            selected_option_id = submitted_data.get(f'answers_{question.id}')
            if selected_option_id:
                try:
                    option = Option.objects.get(id=selected_option_id, question=question)
                    Answer.objects.create(
                        attempt=user_attempt,
                        question=question,
                        selected_option=option
                    )
                    if option.is_correct:
                        result['correct'] += 1
                    else:
                        result['incorrect'] += 1
                except Option.DoesNotExist:
                    return HttpResponseBadRequest("Invalid option submitted.")
            else:
                result['unanswered'] += 1

        user_attempt.score = result['correct']
        user_attempt.completed_at = now()
        user_attempt.save()

        return render(request, 'quiz/quiz_result.html')

    return render(request, 'quiz/attend_quiz.html', {
        'questions': questions,
        'quiz': quiz,
        'time_remaining': int(time_remaining.total_seconds()),
    })





@login_required
def quiz_list(request):
    quizzes = Quiz.objects.filter(created_by=request.user)
    return render(request, 'quiz/quiz_list.html', {'quizzes': quizzes})

@login_required
def create_quiz(request):
    if request.method == 'POST':
        form = QuizForm(request.POST)
        
        # Handling validation for required fields manually
        title = request.POST.get('title')
        description = request.POST.get('description')
        duration = request.POST.get('duration')

        # Basic validation for required fields
        if not title or not description or not duration:
            messages.error(request, "All fields are required.")
            return render(request, 'quiz/create_quiz.html', {'form': form})

        try:
            # Try to convert duration into minutes
            duration_minutes = int(duration) if duration else 0
            duration_obj = timedelta(minutes=duration_minutes) if duration_minutes else None
        except ValueError:
            duration_obj = None

        # Check if quiz with the same title already exists
        if Quiz.objects.filter(title=title).exists():
            messages.error(request, "Quiz with this title already exists.")
            return render(request, 'quiz/create_quiz.html', {'form': form})

        # Create the quiz object
        quiz = Quiz.objects.create(
            title=title,
            description=description,
            created_by=request.user,
            is_timed=True if duration_obj else False,
            duration=duration_obj
        )
        messages.success(request, "Quiz created successfully!")
        return redirect('quiz:quiz_list')

    else:
        form = QuizForm()  # Show an empty form for GET request

    return render(request, 'quiz/create_quiz.html', {'form': form})


@login_required
def edit_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, created_by=request.user)

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        duration = request.POST.get('duration')

        errors = {}

        if not title:
            errors['title'] = "This field is required."
        if not description:
            errors['description'] = "This field is required."
        if not duration:
            errors['duration'] = "This field is required."

        if Quiz.objects.exclude(id=quiz.id).filter(title=title, created_by=request.user).exists():
            messages.error(request, "Another quiz with this title already exists.")
            return render(request, 'quiz/edit_quiz.html', {
                'quiz': quiz,
                'title': title,
                'description': description,
                'duration': duration,
                'errors': errors
            })

        if errors:
            return render(request, 'quiz/edit_quiz.html', {
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
        return redirect('quiz:quiz_list')

    return render(request, 'quiz/edit_quiz.html', {'quiz': quiz})

@login_required
def delete_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, created_by=request.user)
    if request.method == 'POST':
        quiz.delete()
        messages.success(request, "Quiz deleted successfully!")
        return redirect('quiz:quiz_list')
    return render(request, 'quiz/delete_quiz.html', {'quiz': quiz})

