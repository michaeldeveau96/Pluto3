from __future__ import absolute_import, unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .tasks import GetData
import random
import datetime

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter


# Create your views here.
def index(request):
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
    fig = Figure()

    ax = fig.add_subplot(111)
    x=[]
    y=[]
    now = datetime.datetime.now()
    delta = datetime.timedelta(days=1)
    for i in range(10):
        x.append(now)
        now+=delta
        y.append(random.randint(0, 1000))
    ax.plot_date(x, y, '-')
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()
    canvas = FigureCanvas(fig)
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response

    '''fig.scatter(x, y, s=area, marker='o')
    fig.xticks([])
    fig.yticks([])
    fig.plot(x, y, '-o')

    for i, txt in enumerate(devices):
        txt = 'Device Name: ' + str(hostnames[i]) + '\n' + \
              'Device IP: ' + str(devices[i]) + '\n' + \
              'Ping: ' + str(responses[i]) + '\n' + \
              'Download: ' + str(downloads[i]) + '\n' + \
              'Upload: ' + str(uploads[i])
        plt.annotate(txt, (x[i], y[i]))
    canvas = FigureCanvas(fig)
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response'''
    #return HttpResponse(devices)
