from django.urls import path
from quiz.views import answer_question_view,quiz_list,create_quiz,edit_quiz,delete_quiz

app_name="quiz"
urlpatterns = [
    path('<int:quiz_id>/attend/', answer_question_view, name='attend_quiz'),
    path('quizzes/', quiz_list, name='quiz_list'),
    path('quizzes/create/',create_quiz, name='create_quiz'),
    path('<int:quiz_id>/edit/', edit_quiz, name='edit_quiz'),
    path('<int:quiz_id>/delete/',delete_quiz, name='delete_quiz'),
]
