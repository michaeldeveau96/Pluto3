from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from subprocess import PIPE, Popen
from .pluto import main
import time

# Create your views here.
def index(request):
    x = main()
    time.sleep(60)
    return HttpResponse(x)
