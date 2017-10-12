# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import time
from django.shortcuts import get_object_or_404, render,redirect
from django.template import loader
from django.http import HttpResponse
from .models import *
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt

#from django.views.generic.edit import CreateView,UpdateView,DeleteView
#from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import authenticate,login,logout
#from django.views import generic
#from django.views.generic import View
from .forms import UserForm
from .forms import LoginForm
#--------------------------
from django.contrib.auth import get_user_model
from django.http import JsonResponse

from django.views.generic import View

from rest_framework.views import APIView
from rest_framework.response import Response
import time
#--------------------------------
#View to show temperature,humidity,etc. on the webpage
def index(request,pid):
    temp = Temperature.objects.filter(pid=pid)
    humid = Humidity.objects.filter(pid=pid)
    s=temp[len(temp)-1]
    w=humid[len(humid)-1]
    op1=int(s.temperature)
    op2=int(w.humidity)
    depth = Depth.objects.all()
    p=depth[len(depth)-1]
    op3=int(p.depth)
    dept = soilMoisture.objects.filter(pid=pid)
    p=dept[len(dept)-1]
    op4=int(p.moisture)
    rain=Rain.objects.all()
    w=rain[len(rain)-1]
    op6=int(w.rainfall)
    plants=Plant.objects.all()
    for i in plants:
	if(i.id==int(pid)):
		uid=i.user.id
		break
    plants=Plant.objects.filter(user=uid)
    pid=str(pid)
    context = {'temp': op1,'humid':op2, 'depth':op3, 'moist':op4,'pid':pid,'user':uid,'plants':plants,'rain':op6}
    return render(request, 'sensor/index.html', context)
#Checks if no. of recordsis greater than 150 and if true deletes 50 oldest records
def check():
    temp = Temperature.objects.all()
    humid = Humidity.objects.all()
    depth = Depth.objects.all()
    dept = soilMoisture.objects.all()
    if(len(temp)>150):
        for i in range(0,51):
            a=temp[i]
            a.delete()
    if(len(humid)>150):
        for i in range(0,51):
            a=humid[i]
            a.delete()
    if(len(depth)>150):
        for i in range(0,51):
            a=depth[i]
            a.delete()
    if(len(dept)>150):
        for i in range(0,51):
            a=dept[i]
            a.delete()
#It acts as a pseudo view which works with pseudo url .../sensor/m?t=''&h=''&...  Helps in storing data in database.
#
@csrf_exempt
def getdata(request):
    temp=request.GET['t']
    humid=request.GET['h']
    dept=request.GET['d']
    mois = request.GET['mo']
    pi=request.GET['pid']
    rain=request.GET['rain']
    d=time.ctime()
    plant=Plant.objects.filter(id=int(pi))
    f=Temperature(temperature=temp,time=d,pid=plant[0])
    f.save()
    s = Depth(depth=dept,time=d)
    s.save()
    q=Humidity(humidity=humid,time=d,pid=plant[0])
    q.save()
    m=soilMoisture(moisture=mois,time=d,pid=plant[0])
    if(m<=0):
       plant[0].life=0
    plant[0].save()
    m.save()
    s=Rain(rainfall=rain,time=d)
    s.save()
    check()
    return HttpResponse(str(temp))
def logout_user(request):
    logout(request)
    #form = LoginForm(request.POST or None)
    #context = {
     #   "form": form,
    #}
    #return render(request, 'sensor/login.html', context)
    return redirect('/sensor/login_user/')


#View to allow users to register on our Website.
def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
		plants = Plant.objects.filter(user=request.user)
		for p in plants:
			d=soilMoisture.objects.filter(pid=p)
			d=int(d[len(d)-1].moisture)
			if(d!=0):
				d=1
			p.life=d
			p.save()
		plants = Plant.objects.filter(user=request.user)
                #albums = Album.objects.filter(user=request.user)
                return render(request, 'sensor/itws.html',{'username':username,'plants':plants})
    context = {
        "form": form,
    }
    return render(request, 'sensor/signup.html', context)
#This view allows users to login. It gets called when url ~/sensor/login_user is called
def login_user(request):
    form = LoginForm(request.POST or None)
    context = {
        "form": form,
    }
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                plants = Plant.objects.filter(user=request.user)
		for p in plants:
			d=soilMoisture.objects.filter(pid=p)
			d=int(d[len(d)-1].moisture)
			if(d!=0):
				d=1
			p.life=d
			p.save()
		plants = Plant.objects.filter(user=request.user)
                #return render(request, 'sensor/itws.html', {'albums': albums})
                return render(request,'sensor/itws.html',{'username':username,'plants':plants})
            else:
                return render(request, 'sensor/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'sensor/login.html', {'error_message': 'Invalid login'})
    return render(request, 'sensor/login.html',context)
#View to show the first page after login to user.
def home(request,pid):
    plants=Plant.objects.all()
    for i in plants:
	if(i.id==int(pid)):
		uid=i.user.id
		break
    plants = Plant.objects.filter(user=request.user)
    for p in plants:
		d=soilMoisture.objects.filter(pid=p)
		d=int(d[len(d)-1].moisture)
		if(d!=0):
			d=1
		p.life=d
		p.save()
    plants = Plant.objects.filter(user=request.user)
    user=User.objects.filter(id=uid)
    username=user[0].username
    return render(request,'sensor/itws.html',{'username':username,'plants':plants})
#A view just needed to send the data from database to display in index.html
def gen(request):
    temp = Temperature.objects.all()
    humid = Humidity.objects.all()
    s=temp[len(temp)-1]
    w=humid[len(humid)-1]
    op1=int(s.temperature)
    op2=int(w.humidity)
    context = {'temp': op1,'humid':op2}
    return render(request, 'sensor/index.html', context)

#-----------------Today ------------------------------
class HomeView(View):
    def get(self, request, pid):
        
        return render(request, 'sensor/charttemp.html',{'pid':int(pid)})

class HumidView(View):
    def get(self, request,pid, *args, **kwargs):
        
        return render(request, 'sensor/charthumid.html',{'pid':str(pid)})
class MoistView(View):
    def get(self, request,pid, *args, **kwargs):
	
        return render(request, 'sensor/chartmoist.html',{'pid':str(pid)})

def get_data(request, *args, **kwargs):
    h = Depth.objects.all()
    s=h[len(h)-1]
    height=int(s.depth)
    data = {
        'height':height,
    }
    return JsonResponse(data) # http response


class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request,pid, format=None):
        temp = Temperature.objects.filter(pid=pid)
        labels = []
        default_items = []
        for i in temp:
            labels.append(i.time)
            default_items.append(i.temperature)
        data = {
                "labels": labels,
                "default": default_items,
        }
        return Response(data)
class ChartHumidData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request,pid, format=None):
        humid = Humidity.objects.filter(pid=pid)
        labels = []
        default_items = []
        for i in humid:
            labels.append(i.time)
            default_items.append(i.humidity)
        data = {
                "labels": labels,
                "default": default_items,
        }
        return Response(data)
class ChartMoistData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request,pid, format=None):
        humid = soilMoisture.objects.filter(pid=pid)
        labels = []
        default_items = []
        for i in humid:
            labels.append(i.time)
            default_items.append(i.moisture)
        data = {
                "labels": labels,
                "default": default_items,
        }
        return Response(data)
