from django.conf.urls import patterns, url

from constructor import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index')
)
