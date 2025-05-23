from django.db import models
from django.core.validators import MinLengthValidator
from django.utils import timezone
import datetime
from django.contrib import admin


# class Question(models.Model):
#     question_text = models.CharField(unique=True,
#                                      max_length=200, verbose_name="question_text")
#     created_date = models.DateTimeField(verbose_name="created_date")

#     @admin.display(
#         boolean=True,
#         ordering=created_date,
#         description="Created recently?"
#     )
#     def was_created_recently(self):
#         return self.created_date >= timezone.now() - datetime.timedelta(days=2)

#     def __str__(self):
#         return self.question_text


# class Choice(models.Model):
#     question = models.ForeignKey(to=Question, on_delete=models.CASCADE)
#     choice_text = models.CharField(unique=True, verbose_name="choice_text", max_length=200, validators=[
#                                    MinLengthValidator(limit_value=1)])
#     votes = models.IntegerField(verbose_name="votes", default=0)

#     def __str__(self):
#         return self.choice_text


class Split(models.Model):
    split_name = models.CharField(verbose_name="split_name", max_length=100, validators=[
                                  MinLengthValidator(limit_value=1)])
    created_date = models.DateTimeField(
        verbose_name="created_date", auto_now=True)

    def __str__(self):
        return self.split_name

    def get_total_expenses(self):
        return sum(expense.amount for expense in self.expenses.all())


class Participant(models.Model):
    split = models.ForeignKey(
        Split, on_delete=models.CASCADE, related_name='participants')
    participant_name = models.CharField(max_length=100, validators=[
        MinLengthValidator(limit_value=1)])

    def __str__(self):
        return f"{self.participant_name} ({self.split.split_name})"

    def get_balance(self):
        # Calculate how much this participant has paid
        paid = sum(
            expense.amount for expense in self.split.expenses.filter(paid_by=self))

        # Calculate share of all expenses
        total_expenses = self.split.get_total_expenses()
        num_participants = self.split.participants.count()
        if num_participants > 0:
            share = total_expenses / num_participants
        else:
            share = 0

        # Return the balance (positive means others owe this participant)
        return paid - share


class Expense(models.Model):
    split = models.ForeignKey(
        Split, on_delete=models.CASCADE, related_name='expenses')
    description = models.CharField(max_length=200, validators=[
        MinLengthValidator(limit_value=1)])
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    paid_by = models.ForeignKey(
        Participant, on_delete=models.CASCADE, related_name='expenses_paid')
    created_date = models.DateTimeField(
        verbose_name="created_date", auto_now=True)

    def __str__(self):
        return f"{self.description} ({self.amount})"
