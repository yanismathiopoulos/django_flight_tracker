from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
# from .models import Author

# Create your views here.

# from .models import Book, Author, BookInstance, Genre


def index(request):
    """View function for home page of site."""
    # # Generate counts of some of the main objects
    # num_books = Book.objects.all().count()
    # num_instances = BookInstance.objects.all().count()
    # # Available copies of books
    # num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    # num_authors = Author.objects.count()  # The 'all()' is implied by default.

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    # Render the HTML template index.html with the data in the context variable.
    return render(request, 'index.html',
                  context={'num_visits': num_visits})
    # return HttpResponse("<h1>This is the home page</h1>")
