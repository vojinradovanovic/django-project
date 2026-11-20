from django.http import HttpResponse
from django.shortcuts import render

### VIEWS ###

def home(request):
    return render(request, "home.html")