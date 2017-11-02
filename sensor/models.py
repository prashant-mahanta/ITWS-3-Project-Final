# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import datetime 
from django.contrib.auth.models import Permission, User
#Plant class
#This class identifies each plant. A user can have multiple plants
#Life value decides if water is needed to be added to plant
#Life value of 0 represents moisture value 0 which means plant
#immediately needs to be watered. Otherwise it is 1.
class Plant(models.Model):
	user=models.ForeignKey(User,default=1)
	plant_type=models.CharField(max_length=20)
	latitude=models.FloatField(default=13.562975)
	longitude=models.FloatField(default=80.021457)
	life=models.IntegerField(default=1)
	def __str__(self):
        	return self.plant_type
	
#Temperature class
#This class stores the temperature (0c)for each of the plants
#along with the time when it was taken
class Temperature(models.Model):
    temperature = models.CharField(max_length=20)
    time=models.CharField(max_length=50)
    pid = models.ForeignKey(Plant, on_delete=models.CASCADE)
    def __str__(self):
        return self.temperature


#Humidity class
#This class stores humidity value in % (relative humidity)
#along with the time when it was taken
class Humidity(models.Model):
	humidity = models.CharField(max_length=20)
	time = models.CharField(max_length=50)
	pid = models.ForeignKey(Plant, on_delete=models.CASCADE)
	def __str__(self):
        	return self.humidity

#Soil pH class
#This class stores pH value for each plant.
#along with the time when it was taken. Since the plants may be widely 
#separated, we have assumed that pH can change for each of the plants
class soilPH(models.Model):
	pH = models.CharField(max_length=30)
	date = models.CharField(max_length=20)
	pid = models.ForeignKey(Plant, on_delete=models.CASCADE)
	def __str__(self):
        	return self.pH
#soil Moisture
#It stores the soil moisture value in % corresponding to each of the plants
#along with the time when it was taken
class soilMoisture(models.Model):
	moisture = models.CharField(max_length=20)
	time = models.CharField(max_length=20)
	pid = models.ForeignKey(Plant, on_delete=models.CASCADE)
	def __str__(self):
        	return self.moisture
#This class stores the water level of the tank
#along with the time when it was taken
class Depth(models.Model):
	depth = models.CharField(max_length=20)
	time = models.CharField(max_length=20)
	def __str__(self):
		return self.depth
#This class stores the Rain Gauge value(in cm)
#along with the time when it was taken
class Rain(models.Model):
	rainfall = models.CharField(max_length=20)
	time = models.CharField(max_length=20)
	def __str__(self):
		return self.rainfall
