from __future__ import absolute_import, unicode_literals
from django.views.generic import View
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .tasks import GetData
import random
import datetime
import io

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter


# Create your views here.
class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html', {})

def get_data(request, *args, **kwargs):
    task = GetData()
    task.delay()
    task.apply_async()
    res = task.run()
    responses = res[0]
    downloads = res[1]
    uploads = res[2]
    hostnames = res[3]
    x = res[4]
    y = res[5]
    area = res[6]
    devices = res[7]
