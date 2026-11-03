import datetime

from django.contrib import admin
from django.db import models
from django.utils import timezone

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    def get_choices(self):
        return Choice.objects.filter(question=self)
    def get_number_votes(self):
        nombre_vote = 0
        for choice in self.get_choices():
            nombre_vote += choice.votes
        return nombre_vote

class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'pub_date']
    list_filter = ['pub_date']
    ordering = ["-pub_date", "question_text"]
    search_fields = ['question_text', 'pub_date']

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def get_pourcentage(self):
        number_of_votes = self.question.get_number_votes()
        if number_of_votes == 0:
            return 0
        return self.votes/number_of_votes * 100
    def __str__(self):
        return self.choice_text

class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['question','choice_text', 'votes']
    list_filter = ['question', 'votes']
    ordering = ["question", "votes", "choice_text"]
    search_fields = ['question', 'choice_text', 'votes']
