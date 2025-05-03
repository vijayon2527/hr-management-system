from django.db import models
from users.models import User
from django.db.models import Sum

class Quiz(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_quizzes')
    is_active = models.BooleanField(default=True)
    is_timed = models.BooleanField(default=False)
    duration = models.DurationField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['is_active']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return self.title

    @property
    def total_marks(self):
        return self.questions.aggregate(total=Sum('points'))['total'] or 0


class Question(models.Model):
    TEXT = 'text'
    MCQ = 'mcq'
    TYPE_CHOICES = (
        (TEXT, 'Text'),
        (MCQ, 'MCQ'),
    )

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    content = models.TextField()
    points = models.PositiveIntegerField(default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['quiz', 'content'], name='unique_quiz_question')
        ]

    @property
    def get_options(self):
        return self.options.all()

    def __str__(self):
        return f"{self.content} ({self.quiz.title})"


class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['question', 'text'], name='unique_option_text')
        ]

    def __str__(self):
        return self.text

class Attempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attempts')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    score = models.PositiveIntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'quiz'], name='unique_quiz_attempt')
        ]

    @property
    def total_questions(self):
        return self.quiz.questions.count()

    @property
    def percentage(self):
        total = self.total_questions
        if total > 0:
            return round((self.score / total) * 100, 2)
        return 0

    @property
    def result(self):
        return "Pass" if self.percentage >= 70 else "Fail"

    @property
    def time_taken(self):
        if self.started_at and self.completed_at:
            duration = self.completed_at - self.started_at
            return str(duration).split('.')[0]
        return "N/A"


    def __str__(self):
        return f"{self.user}'s attempt on {self.quiz.title}"


class Answer(models.Model):
    attempt = models.ForeignKey(Attempt, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(Option, on_delete=models.SET_NULL, null=True, blank=True)
    answer_text = models.TextField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['attempt', 'question'], name='unique_attempt_question')
        ]

    def __str__(self):
        return f"Answer to {self.question.content} by {self.attempt.user}"
