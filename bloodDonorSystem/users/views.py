from django.shortcuts import render

# Create your views here.


def home_view(request):
    return render(request, 'home.html')


def get_started(request):
    return render(request, 'get-started.html')
