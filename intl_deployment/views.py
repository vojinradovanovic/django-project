from django.shortcuts import render, redirect

from .forms import QueryForm
from .helpers.data_handling import *

### VIEWS ###

def cost_estimate(request):

    # initialise local variables
    data = None
    saved_data = request.session.get("cost_estimate_form_data")

    # if form has been filled out
    if request.method == "POST":
        form = QueryForm(request.POST)  # populate form
        
        if form.is_valid():
            # unpack data from QueryForm
            input = extract_from_QueryForm(form)

            # generate data for output
            data = generate_cost_estimate_data(input)

            # store the data in session
            request.session["cost_estimate_form_data"] = request.POST.dict()

    # if there is saved data from the previous session, retrieve it
    elif saved_data:
        form = QueryForm(saved_data)    # populate form form saved data

    # for any other request, create a blank form
    else:
        form = QueryForm()

    return render(request, "intl_deployment/cost_estimate.html", {"form": form, "data": data})

def immigration(request):

    # get stored data from cost estimate
    saved_data = request.session.get("cost_estimate_form_data")

    # make filling in valid data in cost_estimate the only way of getting to immigration
    if not saved_data:
        return redirect("intl_deployment:cost_estimate")

    form = QueryForm(saved_data)    # populate form form saved data

    if not form.is_valid():
        return redirect("intl_deployment:cost_estimate")

    # unpack data from QueryForm
    input = extract_from_QueryForm(form)

    immigration_data = generate_immigration_data(input)

    return render(request, "intl_deployment/immigration.html", {"immigration_data": immigration_data})