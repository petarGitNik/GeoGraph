# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.shortcuts import render
from django.http import JsonResponse
from .query_dbpedia import get_companies
import json

# Create your views here.
def index(request, latitude = 0.0, longitude = 0.0, tolerance = 0.0, language = 'default'):
    """
    Load the homepage. If user supplies input arguments, query dbpedia, 'parse'
    returned JSON, and display companies on the map.
    """
    if request.method == 'POST':
        latitude = float(request.POST['latitude'])
        longitude = float(request.POST['longitude'])
        tolerance = float(request.POST['tolerance'])
        language = request.POST['language']
        companies = get_companies(latitude, longitude, tolerance, language)

        with open('media/json_file.json', 'w') as f:
            f.write(companies + '\n')

        return render(request, 'geo/index.html', {
            'json_file' : 'media/json_file.json',
        })
    return render(request, 'geo/index.html', {
        'json_file' : 'media/json_file.json',
    })
