from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from .models import Split, Participant, Expense
from django.utils.datastructures import MultiValueDictKeyError
from django.urls import reverse
from django.db.models import F
from django.views import generic


class HomeView(generic.ListView):
    template_name = "splits/home.html"
    context_object_name = "latest_splits"

    def get_queryset(self):
        """Return the last five created splits."""
        return Split.objects.order_by("-created_date")[:5]


# class DetailView(generic.DetailView):
#     model = Question
#     template_name = "splits/detail.html"


# class ResultsView(generic.DetailView):
#     model = Question
#     template_name = "splits/results.html"


# def votes(request, question_id):
#     question = get_object_or_404(Question, id=question_id)
#     try:
#         choice = question.choice_set.get(id=request.POST["choice"])
#     except MultiValueDictKeyError:
#         return render(request, "splits/detail.html", {"question": question, "error_message": "Did'nt select a option"})
#     else:
#         choice.votes = F("votes") + 1
#         choice.save()

#         return HttpResponseRedirect(reverse(viewname="splits:results", args=[question.id]))
