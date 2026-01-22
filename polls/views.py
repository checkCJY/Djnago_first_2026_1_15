from django.utils import timezone
from django.db.models import F
from django.urls import reverse
from django.views import generic
from django.http import HttpResponseRedirect

from django.shortcuts import render, get_object_or_404
from .models import Question, Choice


# 페이지가 없는 경우 띄워주기위해 get_object_or_404

# 기존코드
# def aa(request):
#     latest_question_list = Question.objects.all()
#     choice_list = Choice.objects.all()
#     context = {
#         "question": latest_question_list,
#         "choice": choice_list
#         }
#     return render(request, "polls/aa.html", context)

'''함수버전 index'''
# def index(request):
# 	latest_question_list = Question.objects.order_by("-pub_date")[:5]
# 	context = {"latest_question_list": latest_question_list}
# 	return render(request, "polls/index.html", context)

# 메인 페이지 (질문 목록)
class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())
    

'''함수버전 detail'''
# def detail(request, question_id):
# 	question = get_object_or_404(Question, pk=question_id)
# 	return render(request, "polls/detail.html", {"question": question})

# 질문 상세 페이지
class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"
    context_object_name = "question"

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())
    

'''함수버전 results'''
# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, "polls/results.html", {"question": question})

# 결과 페이지
class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"
    context_object_name = "question"

'''함수버전 vote'''
# def vote(request, question_id):
#     return HttpResponse(f"You're voting on question {question_id}.")


# 투표 처리 로직
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message":"You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
    
