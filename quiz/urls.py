from django.urls import path
from quiz.views import answer_question_view

app_name="quiz"
urlpatterns = [
    path('<int:quiz_id>/attend/', answer_question_view, name='attend_quiz'),
    
]
