# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect

def index(request ):
    return render_to_response("OpenPOP.html", {})