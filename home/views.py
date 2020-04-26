from django.shortcuts import render, redirect
from django.views import generic
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from .forms import AddPositiveNumbersForm, RoundTripForm
from django_flight_tracker.flightsearch import *


def index(request):
    """View function for home page of site."""

    if request.method == 'POST':
        form = RoundTripForm(request.POST)
        if form.is_valid():

            apikey = form.cleaned_data['apikey']
            del form.cleaned_data['apikey']     #TODO: find a better way
            parameters = form.cleaned_data
            content = search(apikey=apikey, parameters=parameters, n=10)

            return render(request, 'result.html', context={'content': content})

    else:
        form = RoundTripForm()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    # Render the HTML template index.html with the data in the context variable.
    return render(request, 'index.html', context={'form': form,
                                                  'num_visits': num_visits})

    # return HttpResponse("<h1>This is the home page</h1>")
