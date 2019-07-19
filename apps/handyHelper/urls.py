from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login$', views.index),
    url(r'^home$', views.home),    
    url(r'^register$', views.register),
    url(r'^validated$', views.login),
    url(r'^home/newjob$', views.newJob),
    url(r'^home/newjob/createjob$', views.createJob),
    url(r'^home/view/(?P<jobID>\d+)', views.view),
    url(r'^home/giveupjob/(?P<jobID>\d+)', views.giveUpJob),
    url(r'^home/addjob/(?P<jobID>\d+)', views.addJob),  
    url(r'^home/removejob/(?P<jobID>\d+)', views.removeJob),  
    url(r'^home/editjob/(?P<jobID>\d+)', views.editJob),  
    url(r'^home/editjob/updatejob/(?P<jobID>\d+)$', views.updateJob),  
    url(r'^home/finishjob/(?P<jobID>\d+)', views.finishJob),
    url(r'^home/logout$', views.logout)

]