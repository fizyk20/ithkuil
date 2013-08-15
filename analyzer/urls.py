from django.conf.urls import patterns, url

from analyzer import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index')
)
