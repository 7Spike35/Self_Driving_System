from django.http import HttpResponse

from django.shortcuts import render

# Create your views here.
from django.shortcuts import render


def re_learn(request):
    return render(request, 're_learn.html')

