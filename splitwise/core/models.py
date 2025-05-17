from django.db import models
from django.contrib.auth.models import User


class Split(models.Model):
    name = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_total_expenses(self):
        return sum(expense.amount for expense in self.expenses.all())


class Participant(models.Model):
    trip = models.ForeignKey(
        Trip, on_delete=models.CASCADE, related_name='participants')
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.trip.name})"

    def get_balance(self):
        # Calculate how much this participant has paid
        paid = sum(
            expense.amount for expense in self.trip.expenses.filter(paid_by=self))

        # Calculate share of all expenses
        total_expenses = self.trip.get_total_expenses()
        num_participants = self.trip.participants.count()
        if num_participants > 0:
            share = total_expenses / num_participants
        else:
            share = 0

        # Return the balance (positive means others owe this participant)
        return paid - share


class Expense(models.Model):
    trip = models.ForeignKey(
        Trip, on_delete=models.CASCADE, related_name='expenses')
    description = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_by = models.ForeignKey(
        Participant, on_delete=models.CASCADE, related_name='expenses_paid')
    date = models.DateField()

    def __str__(self):
        return f"{self.description} ({self.amount})"
