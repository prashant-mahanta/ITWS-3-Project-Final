from __future__ import unicode_literals
import time
from django.shortcuts import get_object_or_404, render,redirect
from django.template import loader
from django.http import HttpResponse

from django.http import Http404
#from sensor.models import *

def index(request):
    #return render(request, 'sensor/itws.html')
    return render(request,'sensor/base.html')
