import datetime

from django.contrib import admin
from django.db import models
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        return self.question_text

    @admin.display(
        boolean=True,
        ordering="pub_date",
        description="Published recently?",
    )
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def age(self):
        difference = timezone.now() - self.pub_date
        return difference.days

    def get_choices(self):
        return Choice.objects.filter(question=self)

    def get_number_votes(self):
        nombre_vote = 0
        for choice in self.get_choices():
            nombre_vote += choice.votes
        return nombre_vote

    def get_choices_with_frequency(self):
        total = 0
        choices = self.choice_set.all()
        for c in choices:
            total += c.votes
        return [(c.choice_text, c.votes, c.votes / total * 100) for c in choices]


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def get_pourcentage(self):
        number_of_votes = self.question.get_number_votes()
        if number_of_votes == 0:
            return 0
        return self.votes / number_of_votes * 100

    def __str__(self):
        return self.choice_text
