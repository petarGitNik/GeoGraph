# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.shortcuts import render
from django.http import JsonResponse
from .query_dbpedia import get_companies

# Create your views here.
def index(request, latitude = 0.0, longitude = 0.0, tolerance = 0.0, language = 'default'):
    if request.method == 'POST':
        latitude = float(request.POST['latitude'])
        longitude = float(request.POST['longitude'])
        tolerance = float(request.POST['tolerance'])
        language = request.POST['language']
        companies = get_companies(latitude, longitude, tolerance, language)

        return render(request, 'geo/index.html', {
            'json_file' : companies
        })
    return render(request, 'geo/index.html', {})
