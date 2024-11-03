from django.shortcuts import render


# Create your views here.
def index(request, *args, **kwargs):
    return render(request, 'frontend/index.html')

def intro_view(request):
    return render(request, 'frontend/intro.html')

