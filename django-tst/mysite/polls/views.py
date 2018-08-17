from django.shortcuts import render
from django.http import HttpResponse
from .models import Question

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = { 'latest_question_list': latest_question_list }
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    return HttpResponse("Your are looking at question %s." % question_id)


def results(request, question_id):
    result = "Your are looking at the results of question %s."
    return HttpResponse(result % question_id)


def vote(request, question_id):
    return HttpResponse("Your are voting on question %s" % question_id)

