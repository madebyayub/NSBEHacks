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
        return TemplateResponse(request, 'main/index.html', context={"youtube_link": id, "id": id})

    elif request.method == 'POST':
        
        pass