from django.shortcuts import render
from django.template.response import TemplateResponse

# Create your views here.


def index(request):
    # User requests the home page
    if request.method == 'GET':
        return TemplateResponse(request, 'main/index.html', context={"example": "-- some data --", "example2": "-- some other data --"})

    elif request.method == 'POST':

        pass

# Create your views here.


def problem(request, id):

    # Handle getting video data

    # User requests the home page
    if request.method == 'GET':
        return TemplateResponse(request, 'main/problem.html',
                                context={"id": id,
                                         "title": "Two Sum",
                                         "categories": ["Array", "Linked List"],
                                         "videos": [
                                             {"title": "Building the Django Base HTML Template (Django Tutorial) | Part 13",
                                              "src": "https://www.youtube.com/embed/LjjujVxI0js"},
                                             {"title": "Building the Django Base HTML Template (Django Tutorial) | Part 13",
                                              "src": "https://www.youtube.com/embed/LjjujVxI0js"},
                                             {"title": "Building the Django Base HTML Template (Django Tutorial) | Part 13",
                                              "src": "https://www.youtube.com/embed/LjjujVxI0js"},
                                             {"title": "Building the Django Base HTML Template (Django Tutorial) | Part 13",
                                              "src": "https://www.youtube.com/embed/LjjujVxI0js"}]})
