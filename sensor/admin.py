# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *
admin.site.register(Plant)
admin.site.register(Temperature)
admin.site.register(Humidity)
admin.site.register(soilMoisture)
admin.site.register(Depth)
admin.site.register(Rain)
# Register your models here.
