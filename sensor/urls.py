from django.conf.urls import url
from . import views
from .views import *
app_name = 'sensor'
urlpatterns = [
    # ex: /polls/
    url(r'^(?P<pid>[0-9]+)$', views.index, name='index'),url(r'^m$',views.getdata,name="getdata"),   
    url(r'^gen/$', views.gen, name='gen'),
    #Register url
    url(r'^register/$',views.register,name="register"),
    #Login url
    url(r'^login_user/$', views.login_user, name='login_user'),
    #Logout url
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^(?P<pid>[0-9]+)/home/$', views.home, name='main-home'),
    #temperature for graph
    url(r'^(?P<pid>[0-9]+)/temp/$', HomeView.as_view(), name='home'),
    url(r'^(?P<pid>[0-9]+)/api/chart/data/$', ChartData.as_view(),name="api-da"),
    #Humidity for graph
    url(r'^(?P<pid>[0-9]+)/humid/$', HumidView.as_view(), name='home-humid'),
    url(r'^(?P<pid>[0-9]+)/api/chart1/data/$', ChartHumidData.as_view(),name="api-humid-da"),

    #Moisture for graph
    url(r'^(?P<pid>[0-9]+)/moist/$', MoistView.as_view(), name='home-moist'),
    url(r'^(?P<pid>[0-9]+)/api/chart2/data/$', ChartMoistData.as_view(),name="api-moist-da"),


    #sending data to the index.html
    url(r'^api/data/$', get_data, name='api-data'),


]
