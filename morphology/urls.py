from django.conf.urls import patterns, url

from morphology import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^category/(?P<cat_id>\d+)/$', views.category, name='category'),
	url(r'^cat_val/(?P<val_id>\d+)/$', views.cat_val, name='cat_val')
)
