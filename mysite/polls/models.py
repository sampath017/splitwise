from django.db import models
from django.core.validators import MinLengthValidator
from django.utils import timezone
import datetime
from django.contrib import admin


class Question(models.Model):
    question_text = models.CharField(unique=True,
                                     max_length=200, verbose_name="question_text")
    created_date = models.DateTimeField(verbose_name="created_date")

    @admin.display(
        boolean=True,
        ordering=created_date,
        description="Created recently?"
    )
    def was_created_recently(self):
        return self.created_date >= timezone.now() - datetime.timedelta(days=2)

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(to=Question, on_delete=models.CASCADE)
    choice_text = models.CharField(unique=True, verbose_name="choice_text", max_length=200, validators=[
                                   MinLengthValidator(limit_value=1)])
    votes = models.IntegerField(verbose_name="votes", default=0)

    def __str__(self):
        return self.choice_text
