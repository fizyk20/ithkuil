from django.http import Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404

from morphology.models import *

def home(request):
	return render(request, 'morphology/index.html', {})

def index(request, *args):
	cats = Category.objects.order_by('name').all()
	return render(request, 'morphology/morph.html', {'categories': cats})
	
def category(request, cat_id):
	cat = get_object_or_404(Category, pk=cat_id)
	context = { 
		'category': cat,
		'values': cat.values.all() 
	}
	return render(request, 'morphology/category.html', context)
	
def cat_val(request, val_id):
	val = get_object_or_404(CategValue, pk=val_id)
	context = { 
		'value': val
	}
	return render(request, 'morphology/cat_val.html', context)

