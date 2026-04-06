from django.http import HttpResponse
import os

# Create your views here.
def home(request):
    ENV = os.getenv('ENVIRONMENT', 'development')
    return HttpResponse(f"Welcome to the home page! Environment: {ENV}")
