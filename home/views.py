from django.shortcuts import render, redirect
from django.views import generic
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from .forms import RoundTripForm
from django_flight_tracker.flightsearch import *


def index(request):
    """View function for home page of site."""

    if request.method == 'POST':
        form = RoundTripForm(request.POST)
        if form.is_valid():

            parameters = {k: v for (k, v) in form.cleaned_data.items() if
                          k not in ('apikey', 'num_results') and
                          v is not None}

            content = search(flight_type=form.cleaned_data['flight_type'],
                             apikey=form.cleaned_data['apikey'],
                             n=form.cleaned_data['num_results'],
                             parameters=parameters)

            print(content)

            if content is None:
                r = render(request, 'unsuccessful_request.html',
                           context={'message': 'Oops, your inputs were not valid, try again!'})
            elif content == {}:
                r = render(request, 'unsuccessful_request.html',
                           context={'message': 'There are no results with these inputs'})
            else:
                r = render(request, 'result.html',
                           context={
                               'content': content
                           })

            return r

    else:
        form = RoundTripForm()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    # Render the HTML template index.html with the data in the context variable.
    return render(request, 'index.html', context={'form': form, 'num_visits': num_visits})
