from django.http import Http404, HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404

def index(request):
	return HttpResponse('Hello World!')
