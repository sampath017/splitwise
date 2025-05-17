from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from .models import Trip, Participant, Expense
from .forms import TripForm, ParticipantForm, ExpenseForm


def home(request):
    trips = Trip.objects.all()
    return render(request, 'expense_splitter/home.html', {'trips': trips})


def expense_detail(request, pk):
    trip = get_object_or_404(Trip, pk=pk)
    expenses = trip.expenses.all()
    participants = trip.participants.all()

    # Calculate balances for each participant
    balances = []
    for participant in participants:
        balance = participant.get_balance()
        balances.append({
            'participant': participant,
            'balance': balance
        })

    # Find who owes who
    settlements = calculate_settlements(participants)

    return render(request, 'expense_splitter/trip_detail.html', {
        'trip': trip,
        'expenses': expenses,
        'participants': participants,
        'balances': balances,
        'settlements': settlements,
    })


def calculate_settlements(participants):
    # Create a list of (participant, balance) tuples
    balances = [(p, p.get_balance()) for p in participants]

    # Sort by balance (ascending for debtors, descending for creditors)
    creditors = sorted([b for b in balances if b[1] > 0], key=lambda x: -x[1])
    debtors = sorted([b for b in balances if b[1] < 0], key=lambda x: x[1])

    # Calculate settlements
    settlements = []
    for debtor, debt in debtors:
        debt = abs(debt)  # Make debt positive
        while debt > 0.01:  # Account for floating point errors
            creditor, credit = creditors[0]
            amount = min(debt, credit)

            settlements.append({
                'from': debtor,
                'to': creditor,
                'amount': amount
            })

            debt -= amount
            creditors[0] = (creditor, credit - amount)

            # If creditor is fully paid, remove them from the list
            if creditors[0][1] < 0.01:
                creditors.pop(0)

    return settlements


def create_trip(request):
    if request.method == 'POST':
        form = TripForm(request.POST)
        if form.is_valid():
            trip = form.save()
            messages.success(request, 'Trip created successfully!')
            return redirect('add_participant', trip.id)
    else:
        form = TripForm()

    return render(request, 'expense_splitter/create_trip.html', {'form': form})


def add_participant(request, trip_id):
    trip = get_object_or_404(Trip, pk=trip_id)

    if request.method == 'POST':
        form = ParticipantForm(request.POST)
        if form.is_valid():
            participant = form.save(commit=False)
            participant.trip = trip
            participant.save()

            if 'add_another' in request.POST:
                return redirect('add_participant', trip.id)
            else:
                return redirect('trip_detail', trip.id)
    else:
        form = ParticipantForm()

    participants = trip.participants.all()
    return render(request, 'expense_splitter/add_participant.html', {
        'form': form,
        'trip': trip,
        'participants': participants
    })


def add_expense(request, trip_id):
    trip = get_object_or_404(Trip, pk=trip_id)

    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.trip = trip
            expense.save()

            if 'add_another' in request.POST:
                return redirect('add_expense', trip.id)
            else:
                return redirect('trip_detail', trip.id)
    else:
        form = ExpenseForm()
        # Only show participants of this trip in the dropdown
        form.fields['paid_by'].queryset = trip.participants.all()

    return render(request, 'expense_splitter/add_expense.html', {
        'form': form,
        'trip': trip
    })


def edit_expense(request, expense_id):
    expense = get_object_or_404(Expense, pk=expense_id)
    trip = expense.trip

    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            messages.success(request, 'Expense updated successfully!')
            return redirect('trip_detail', trip.id)
    else:
        form = ExpenseForm(instance=expense)
        # Only show participants of this trip in the dropdown
        form.fields['paid_by'].queryset = trip.participants.all()

    return render(request, 'trips/edit_expense.html', {
        'form': form,
        'expense': expense,
        'trip': trip
    })


def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, pk=expense_id)
    trip_id = expense.trip.id

    if request.method == 'POST':
        expense.delete()
        messages.success(request, 'Expense deleted successfully!')
        return redirect('trip_detail', trip_id)

    return render(request, 'trips/delete_expense_confirmation.html', {
        'expense': expense
    })
