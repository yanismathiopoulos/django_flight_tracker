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

            print(form)
            print(form.cleaned_data)

            apikey = form.cleaned_data['apikey']
            del form.cleaned_data['apikey']  # TODO: find a better way
            parameters = form.cleaned_data
            content = search(apikey=apikey, parameters=parameters, n=10)
            if content is not None:
                r = render(request, 'result.html', context={'content': content,
                                                            'form_object': form,
                                                            'form_object_cleaned_data': form.cleaned_data})
            else:
                r = render(request, 'unsuccessful_request.html')

            return r

    else:
        form = RoundTripForm()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    # Render the HTML template index.html with the data in the context variable.
    return render(request, 'index.html', context={'form': form, 'num_visits': num_visits})

