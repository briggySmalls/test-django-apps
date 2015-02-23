from django.shortcuts import render
from homepage.models import HomePage


# Create your views here.
def index(request):
    # Get the HomePage
    # NOTE: if HomePage becomes simply 'page' then probably want to
    # get the page instance by searching by title...with nothing
    # mapping to pk=1, i.e the homepage
    homepage = HomePage.objects.first()
    # prepare the context of the template
    context = {
        'homepage': homepage,
    }
    return render(request, 'homepage/index.html', context)
