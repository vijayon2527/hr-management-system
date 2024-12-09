from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from quiz.models import Quiz, Question, Attempt, Answer, Option
from django.utils.timezone import now
import datetime

def answer_question_view(request, quiz_id):
    # Fetch the quiz and related questions
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.prefetch_related('options').all()

    # # Calculate time remaining
    # quiz_duration = datetime.timedelta(minutes=25)  # 25 minutes for the quiz
    # user_attempt, created = Attempt.objects.get_or_create(user=request.user, quiz=quiz)

    # if created:
    #     # Set the start time for the new attempt
    #     user_attempt.started_at = now()
    #     user_attempt.save()
    # # else:
    # #     text = "<h1 style='color:red; text-align: center;'>You already have submitted the quiz!</h1>"
    # #     return HttpResponseBadRequest(text)

    # # Calculate time left
    # elapsed_time = now() - user_attempt.started_at
    # time_remaining = quiz_duration - elapsed_time
    # if time_remaining.total_seconds() <= 0:
    #     # Quiz time expired
    #     return JsonResponse({'error': 'Time is up! Quiz submission is not allowed.'}, status=400)

    # # Handle POST (submitting answers)
    # if request.method == 'POST':
    #     submitted_data = request.POST
    #     result = {'total': len(questions), 'correct': 0, 'incorrect': 0, 'unanswered': 0}

    #     for question in questions:
    #         submitted_options = submitted_data.getlist(f'answers_{question.id}', [])
    #         if submitted_options:
    #             for option_id in submitted_options:
    #                 try:
    #                     option = Option.objects.get(id=option_id, question=question)
    #                     Answer.objects.create(
    #                         attempt=user_attempt,
    #                         question=question,
    #                         selected_option=option
    #                     )
    #                     if option.is_correct:
    #                         result['correct'] += 1
    #                     else:
    #                         result['incorrect'] += 1
    #                 except Option.DoesNotExist:
    #                     return HttpResponseBadRequest("Invalid option submitted.")
    #         else:
    #             result['unanswered'] += 1

    #     # Update attempt score and completion time
    #     user_attempt.score = result['correct']
    #     user_attempt.completed_at = now()
    #     user_attempt.save()

    #     # Return results as JSON
    #     return JsonResponse({
    #         'message': 'Quiz submitted successfully.',
    #         'result': result,
    #         'score': user_attempt.score,
    #         'total_questions': result['total'],
    #     })

    # GET: Render the quiz page with remaining time
    return render(request, 'quiz/attend_quiz.html', {
        'questions': questions,
        'quiz': quiz,
        # 'time_remaining': int(time_remaining.total_seconds()),  # Pass seconds to the template
    })
