from django.contrib import admin

from .models import Quiz, Question, Option, Answer, Attempt


admin.site.register((Quiz, Question, Option, Answer, Attempt))