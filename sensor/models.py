# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import datetime 
from django.contrib.auth.models import Permission, User
class Plant(models.Model):
	user=models.ForeignKey(User,default=1)
	plant_type=models.CharField(max_length=20)
	life=models.IntegerField(default=1)
	def __str__(self):
        	return self.plant_type
	
#Temperature class
#data will be taken after every half an hour
class Temperature(models.Model):
    temperature = models.CharField(max_length=20)
    time=models.CharField(max_length=50)
    pid = models.ForeignKey(Plant, on_delete=models.CASCADE)
    def __str__(self):
        return self.temperature


#Humidity class
#data will be taken after every half an hour
class Humidity(models.Model):
	humidity = models.CharField(max_length=20)
	time = models.CharField(max_length=50)
	pid = models.ForeignKey(Plant, on_delete=models.CASCADE)
	def __str__(self):
        	return self.humidity

#Soil pH class
#will be calculated day wise
class soilPH(models.Model):
	pH = models.CharField(max_length=30)
	date = models.CharField(max_length=20)
	pid = models.ForeignKey(Plant, on_delete=models.CASCADE)
	def __str__(self):
        	return self.pH
#soil Moisture
#will be calculated every half an hour
class soilMoisture(models.Model):
	moisture = models.CharField(max_length=20)
	time = models.CharField(max_length=20)
	pid = models.ForeignKey(Plant, on_delete=models.CASCADE)
	def __str__(self):
        	return self.moisture
class Depth(models.Model):
	depth = models.CharField(max_length=20)
	time = models.CharField(max_length=20)
	def __str__(self):
		return self.depth
class Rain(models.Model):
	rainfall = models.CharField(max_length=20)
	time = models.CharField(max_length=20)
	def __str__(self):
		return self.rainfall
