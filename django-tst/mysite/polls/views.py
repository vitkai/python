# from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hi there! You are at the polls index.")


def detail(request, question_id):
    return HttpResponse("Your are looking at question %s." % question_id)


def results(request, question_id):
    result = "Your are looking at the results of question %s."
    return HttpResponse(result % question_id)


def vote(request, question_id):
    return HttpResponse("Your are voting on question %s" % question_id)

