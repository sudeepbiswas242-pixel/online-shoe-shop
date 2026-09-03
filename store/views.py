

# Create your views here.
from django.shortcuts import render
from .models import Shoe


def home(request):
    shoes = Shoe.objects.all()
    return render(request, 'home.html', {'shoes': shoes})