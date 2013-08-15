from django.http import Http404, HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404

from analyzer.word_splitter import analyze_word

def index(request):
	data = {}
	if 'sentence' in request.POST:
		sentence = request.POST['sentence']
		words = sentence.split()
		result = []
		for word in words:
			slots = analyze_word(word)
			result.append(str(slots))
		data['result'] = result
		return render(request, 'analyzer/index_display.html', data)
	else:
		return render(request, 'analyzer/index_form.html', data)
