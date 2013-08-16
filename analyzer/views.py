from django.http import Http404, HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404

from analyzer.word_splitter import analyze_word

class WrapElement:
	def __init__(self, key, val):
		self.key = key
		self.value = val

class Wrapper:
	def __init__(self, d):
		self.d = d
		
	def __getattr__(self, i):
		if i not in self.d:
			raise AttributeError()
		return self.d[i]
		
	def __iter__(self):
		for k in self.d:
			o = WrapElement(k, self.d[k])
			yield o

def index(request):
	data = {}
	if 'sentence' in request.POST:
		sentence = request.POST['sentence']
		words = sentence.split()
		result = []
		for word in words:
			slots = analyze_word(word)
			result.append(Wrapper(slots))
		data['result'] = result
		return render(request, 'analyzer/index_display.html', data)
	else:
		return render(request, 'analyzer/index_form.html', data)
