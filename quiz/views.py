from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseBadRequest
from quiz.models import Quiz, Attempt, Answer, Option
from django.utils.timezone import now
from django.http import Http404
from users.models import User
from agphr.utils.decorators import allow_access_to


# @allow_access_to([User.APPLICANT_USER])
def answer_question_view(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, is_active=True)

    questions = quiz.questions.prefetch_related('options').all()
    if not questions.exists():
        raise Http404("No questions found for this quiz.")
    
    quiz_duration = quiz.duration
    if not quiz_duration:
        raise Http404("No time duration mentioned to this quiz")
    
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
                    answer = Answer.objects.create(
                        attempt=user_attempt,
                        question=question,
                        selected_option=option
                    )
                    if option.is_correct:
                        user_attempt.score+=1
                        user_attempt.save()
                        
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





