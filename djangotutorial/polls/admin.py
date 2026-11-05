from django.contrib import admin

from polls.models import Question, Choice

class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'pub_date']
    list_filter = ['pub_date']
    ordering = ["-pub_date", "question_text"]
    search_fields = ['question_text', 'pub_date']

class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['question','choice_text', 'votes']
    list_filter = ['question', 'votes']
    ordering = ["question", "votes", "choice_text"]
    search_fields = ['question', 'choice_text', 'votes']

admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)