import json
import os
from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError
from quiz.models import Quiz, Question, Option
from users.models import User

class Command(BaseCommand):
    help = 'Imports a quiz with questions and options from a JSON file'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            default='data/questions.json',
            help='Path to the JSON file containing quiz data'
        )
        parser.add_argument(
            '--mobile',
            type=str,
            default='1234567890',
            help='mobile of the user who created the quiz'
        )
        parser.add_argument(
            '--quiz-title',
            type=str,
            default='Python Basic Quiz',
            help='Title of the quiz to create'
        )

    def handle(self, *args, **options):
        file_path = options['file']
        mobile = options['mobile']
        quiz_title = options['quiz_title']

        # Validate file existence
        if not os.path.exists(file_path):
            raise CommandError(f"File {file_path} does not exist")

        # Load JSON data
        try:
            with open(file_path, 'r') as f:
                quiz_data = json.load(f)
        except json.JSONDecodeError:
            raise CommandError(f"Invalid JSON format in {file_path}")

        # Get or validate user
        try:
            user = User.objects.get(mobile=mobile)
        except User.DoesNotExist:
            raise CommandError(f"User '{mobile}' does not exist. Please create the user first.")

        # Create or get quiz
        try:
            quiz = Quiz.objects.create(
                title=quiz_title,
                description="A comprehensive quiz with 100 Python questions.",
                created_by=user,
                is_active=True,
                is_timed=False
            )
            self.stdout.write(self.style.SUCCESS(f"Created quiz: {quiz.title}"))
        except IntegrityError:
            self.stdout.write(self.style.WARNING(f"Quiz '{quiz_title}' already exists. Using existing quiz."))
            quiz = Quiz.objects.get(title=quiz_title)

        # Process questions and options
        questions_created = 0
        options_created = 0
        for q_data in quiz_data:
            try:
                # Validate question data
                if not all(key in q_data for key in ['content', 'question_type', 'points', 'options']):
                    self.stdout.write(self.style.ERROR(f"Invalid question format: {q_data.get('content', 'Unknown')}"))
                    continue
                if q_data['question_type'] != Question.MCQ:
                    self.stdout.write(self.style.WARNING(f"Skipping non-MCQ question: {q_data['content']}"))
                    continue
                if len(q_data['options']) != 5:
                    self.stdout.write(self.style.ERROR(f"Question '{q_data['content']}' must have exactly 5 options"))
                    continue
                if sum(1 for opt in q_data['options'] if opt['is_correct']) != 1:
                    self.stdout.write(self.style.ERROR(f"Question '{q_data['content']}' must have exactly one correct option"))
                    continue

                # Create question
                question = Question.objects.create(
                    quiz=quiz,
                    question_type=q_data['question_type'],
                    content=q_data['content'],
                    points=q_data['points']
                )
                questions_created += 1
                self.stdout.write(self.style.SUCCESS(f"Created question: {question.content}"))

                # Create options
                for opt_data in q_data['options']:
                    Option.objects.create(
                        question=question,
                        text=opt_data['text'],
                        is_correct=opt_data['is_correct']
                    )
                    options_created += 1
                    self.stdout.write(f"Created option: {opt_data['text']} for {question.content}")

            except IntegrityError as e:
                self.stdout.write(self.style.ERROR(f"Error creating question '{q_data.get('content', 'Unknown')}': {e}"))
                continue

        self.stdout.write(self.style.SUCCESS(
            f"Import completed: {questions_created} questions and {options_created} options created for quiz '{quiz.title}'"
        ))
        self.stdout.write(self.style.SUCCESS(f"Total marks for quiz: {quiz.total_marks}"))