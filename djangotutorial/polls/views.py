from typing import ClassVar
from django.db.models import F, Max, Sum
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views import generic

from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by("-pub_date")[:5]


class AllView(generic.ListView):
    template_name = "polls/all.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by("-pub_date")


ChoiceFormSet = inlineformset_factory(
    Question,
    Choice,
    fields=["choice_text"],
    extra=3,
    min_num=2,
    validate_min=True,
    can_delete=False,
)

class FormPollView(generic.CreateView):
    model = Question
    fields: ClassVar[list[str]] = ["question_text"]
    template_name = "polls/form.html"
    success_url = reverse_lazy("polls:index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["formset"] = ChoiceFormSet()
        return context

    def form_valid(self, form):
        formset = ChoiceFormSet(self.request.POST)

        if not formset.is_valid():
            return self.render_to_response(self.get_context_data(form=form))

        form.instance.pub_date = timezone.now()
        self.object = form.save()

        formset.instance = self.object
        formset.save()

        return HttpResponseRedirect(self.get_success_url())


class StatisticsView(generic.TemplateView):
    template_name = "polls/statistics.html"
    context_object_name = "Statistics"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_questions"] = Question.objects.count()
        context["total_choices"] = Choice.objects.count()
        context["total_votes"] = Choice.objects.aggregate(total_votes=Sum("votes"))[
            "total_votes"
        ]
        context["avg_votes_par_question"] = (
            context["total_votes"] / context["total_questions"]
        )
        last_date = Question.objects.aggregate(last_date=Max("pub_date"))["last_date"]
        context["last_question_saved"] = Question.objects.filter(
            pub_date=last_date
        ).first()
        return context


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


class FrequencyView(generic.DetailView):
    model = Question

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["frequencies"] = self.object.get_choices_with_frequency()

        return context

    template_name = "polls/frequency.html"


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )

    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))


"""
def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    template = loader.get_template("polls/index.html")
    context = {"latest_question_list": latest_question_list}
    return HttpResponse(template.render(context, request))
"""
'''
# Or shorcut
def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": latest_question_list}
    return render(request, "polls/index.html", context)
# Create your views here.
def detail(request, question_id):
    """
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, "polls/detail.html", {"question": question})
    """
    # Or Shortcut
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})

def frequency(request, question_id):
    print(question_id)
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/frequency.html", {"question": question})
'''
