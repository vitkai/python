from django.shortcuts import render
from django.http import Http404, HttpResponse
from .models import Question

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = { 'latest_question_list': latest_question_list }
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    #return HttpResponse("Your are looking at question %s." % question_id)
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question %s doesn't exist." % question_id)
    return render(request, 'polls/detail.html', {'question': question})



def results(request, question_id):
    result = "Your are looking at the results of question %s."
    return HttpResponse(result % question_id)


def vote(request, question_id):
    return HttpResponse("Your are voting on question %s" % question_id)

