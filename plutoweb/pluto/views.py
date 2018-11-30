from __future__ import absolute_import, unicode_literals

from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import View
from rest_framework.response import Response
from rest_framework.views import APIView

from .tasks import GetData


# Create your views here.
class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html', {})

def get_data(request, *args, **kwargs):
    data = {
        "sales": 100,
        "customers": 10,
    }
    return JsonResponse(data)

# REST framework to call tasks
class ChartData(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        task = GetData()
        task.delay()
        task.apply_async()
        res = task.run()
        responses = res[0]
        downloads = res[1]
        uploads = res[2]
        hostnames = res[3]
        phealth = res[4]
        dhealth = res[5]
        uhealth = res[6]
        devices = res[7]
        x = res[8]
        y = res[9]

        pbackgroundColor = []
        pborderColor = []
        dbackgroundColor = []
        dborderColor = []
        ubackgroundColor = []
        uborderColor = []
        for n in phealth:
            if 'HIGH' in n:
                pbackgroundColor.append('rgb(255, 35, 35, 0.2)')
                pborderColor.append('rgb(255, 0, 0, 1)')
            elif "NORMAL" in n:
                pbackgroundColor.append('rgb(0, 206, 34, 0.2)')
                pborderColor.append('rgb(0, 140, 23, 1)')
        for n in dhealth:
            if 'LOW' in n:
                dbackgroundColor.append('rgb(255, 35, 35, 0.2)')
                dborderColor.append('rgb(255, 0, 0, 1)')
            elif "NORMAL" in n:
                dbackgroundColor.append('rgb(0, 206, 34, 0.2)')
                dborderColor.append('rgb(0, 140, 23, 1)')
        for n in uhealth:
            if 'LOW' in n:
                ubackgroundColor.append('rgb(255, 35, 35, 0.2)')
                uborderColor.append('rgb(255, 0, 0, 1)')
            elif "NORMAL" in n:
                ubackgroundColor.append('rgb(0, 206, 34, 0.2)')
                uborderColor.append('rgb(0, 140, 23, 1)')
        data = {
            "hostnames": hostnames,
            "IP": devices,
            "ping": responses,
            "download": downloads,
            "uploads": uploads,
            "pbackgroundColor": pbackgroundColor,
            "pborderColor": pborderColor,
            "dbackgroundColor": dbackgroundColor,
            "dborderColor": dborderColor,
            "ubackgroundColor": ubackgroundColor,
            "uborderColor": uborderColor,
            "x": x,
            "y": y

        }

        return Response(data)


