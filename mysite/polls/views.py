from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from .models import Question


def index(request):
    latest_questions = Question.objects.order_by("-created_date")[:5]
    context = {"latest_questions": latest_questions}

    return render(request, "polls/index.html", context)


def detail(request, question_id):
    question = get_object_or_404(Question, id=question_id)

    return render(request, "polls/detail.html", {"question": question})


def results(request, question_id):
    return HttpResponse(f"You are looking at the results of question {question_id}")


def votes(request, question_id):
    return HttpResponse(f"You are looking at the votes of question {question_id}")
