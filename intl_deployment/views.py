from django.http import HttpResponse
from django.shortcuts import render

### VIEWS ###

def cost_estimate(request):
    return HttpResponse("Cost estimates go here.")

def immigration(request):
    return HttpResponse("Immigration goes here.")