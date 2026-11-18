from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from .forms import QueryForm
from .helpers.data_handling import *

### VIEWS ###

def cost_estimate(request):

    # initialise local variables
    data = None

    # if form has been filled out
    if request.method == "POST":
        form = QueryForm(request.POST)  # populate form
        
        if form.is_valid():
            # unpack data from QueryForm
            input = extract_from_QueryForm(form)

            # generate data for output
            data = generate_cost_estimate_data(input)

    # for any other request, create a blank form
    else:
        form = QueryForm()

    return render(request, "intl_deployment/cost_estimate.html", {"form": form, "data": data})

def immigration(request):
    return HttpResponse("Immigration goes here.")