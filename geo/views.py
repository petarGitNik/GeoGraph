# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def index(request, latitude = 0.0, longitude = 0.0, tolerance = 0.0, language = 'default'):
    if request.method == 'POST':
        pass

    return render(request, 'geo/index.html', {})

def get_companies(request):
    return JsonResponse({'foo' : 'bar'})
