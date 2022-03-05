from django.shortcuts import render
from django.template.response import TemplateResponse

# Create your views here.
def index(request):
    # User requests the home page
    if request.method == 'GET':
        return TemplateResponse(request, 'main/index.html', context={"example": "-- some data --"})

    elif request.method == 'POST':
        pass