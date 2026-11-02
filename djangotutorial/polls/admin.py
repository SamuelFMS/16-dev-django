from django.contrib import admin

from .models import Question, QuestionAdmin
from .models import Choice, ChoiceAdmin

admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)