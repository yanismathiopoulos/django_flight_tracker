from django.shortcuts import render, redirect
from django.views import generic
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from .forms import FlightSearchInputForm
from django_flight_tracker.flightsearch import *
import os


def index(request):
    """View function for home page of site."""

    if request.method == 'POST':
        form = FlightSearchInputForm(request.POST)

        if form.is_valid():

            form = form.clean()

            parameters = {k: v for (k, v) in form.items() if
                          k not in 'num_results' and v is not None}

            apikey = get_apikey()

            if apikey is None:
                r = render(request, 'unsuccessful_request.html',
                           context={'message': 'You need an API key, request one here: https://tequila.kiwi.com/'})

            else:
                content = search(flight_type=form['flight_type'],
                                 apikey=apikey,
                                 n=form['num_results'],
                                 parameters=parameters)

                # print(content)

                if content is None:
                    r = render(request, 'unsuccessful_request.html',
                               context={'message': 'Oops, your inputs were not valid, try again!'})
                elif content == {}:
                    r = render(request, 'unsuccessful_request.html',
                               context={'message': 'There are no results with these inputs'})
                else:
                    r = render(request, 'result.html',
                               context={'content': content})

            return r

    else:
        form = FlightSearchInputForm()

    # Render the HTML template index.html with the data in the context variable.
    return render(request, 'index.html', context={'form': form})
