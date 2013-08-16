from django.http import Http404, HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404

from analyzer.word_splitter import analyze_word
from morphology.models import *

def index(request):
	data = {}
	if 'sentence' in request.POST:
		sentence = request.POST['sentence']
		words = sentence.split()
		result = []
		for word in words:
			slots = analyze_word(word)
			if 'error' in slots:
				return render(request, 'analyzer/index_error.html', slots)
			slots['word'] = word
			result.append(slots)
		data['result'] = []
		for r in result:
			d = {}
			d['word'] = r['word']
			d['type'] = r['type']
			del r['word']
			del r['type']
			# describe each category
			d['categories'] = [('Root', r['VII'])]
			del r['VII']
			for k in r:
				morphemes = Morpheme.objects.filter(slot__word_type__name=d['type']).filter(slot__number=k).filter(content=r[k]).all()
				if len(morphemes) > 1:
					raise Exception('Too many morphemes')
				elif len(morphemes) == 0:
					d['categories'].append((k, r[k]))
					continue
				else:
					morpheme = morphemes[0]
				for val in morpheme.values.all():
					d['categories'].append((val.category.name, val))
			data['result'].append(d)
					
		return render(request, 'analyzer/index_display.html', data)
	else:
		return render(request, 'analyzer/index_form.html', data)
