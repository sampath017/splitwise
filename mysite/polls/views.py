from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from .models import Question
from django.utils.datastructures import MultiValueDictKeyError
from django.urls import reverse
from django.db.models import F
from django.views import generic


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_questions"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by("-created_date")[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


def votes(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    try:
        choice = question.choice_set.get(id=request.POST["choice"])
    except MultiValueDictKeyError:
        return render(request, "polls/detail.html", {"question": question, "error_message": "Did'nt select a option"})
    else:
        choice.votes = F("votes") + 1
        choice.save()

        return HttpResponseRedirect(reverse(viewname="polls:results", args=[question.id]))
