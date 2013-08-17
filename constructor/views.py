from django.http import Http404, HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404

from analyzer.word_splitter import analyze_word
from analyzer.describers import describe_word
from morphology.models import *

def index(request):
	return render(request, 'constructor/index.html', {})
