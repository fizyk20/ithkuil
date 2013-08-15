#!/usr/bin/env python
import http.client
from downloaders.table_parser import TableParser, reformat, replace_h
from morphology.models import *

sess = http.client.HTTPConnection('ithkuil.net', 80)

print('Downloading tables from ithkuil.net...')

sess.request('GET', '/05_verbs_1.html')
res = sess.getresponse()
html = res.read()

print('Downloaded.')
print('Parsing...')

parser = TableParser()
parser.feed(str(html))

def test_table(node):
	try:
		return node.tr[0].td[1].__data__ == 'MOOD'
	except:
		return False
	
print('Parsed.')
print('Filtering for morphology tables...')

result2 = list(filter(test_table, parser.result))

print('Filtered.')
print('Reading data...')

def read_table(node):
	result = []
	moods = []
	illocs = ['ASR', 'DIR', 'IRG', 'ADM', 'HOR', 'DEC']
	for td in node.tr[1].td:
		if not 'ILLOCUTION' in td.__data__:
			moods.append(td.__data__.replace(' ',''))
			
	for i in range(2, len(node.tr)):
		for j in range(1, len(node.tr[i].td)):
			mood = moods[j-1]
			ill = illocs[i-2]
			slots = node.tr[i].td[j].__data__.replace(' ','').replace('-','').split('/')
			for s in slots:
				if s != '—':
					result.append({'mood': mood, 'illocution': ill, 'slot': s})
	return result

morph_dict = []
for node in result2:
	morph_dict += read_table(node)
	
print('Data read.')
print('Saving...')

def value(code, cat):
	try:
		res = CategValue.objects.get(code=code)
	except CategValue.DoesNotExist:
		res = CategValue(code=code, category=Category.objects.get(name=cat))
		res.save()
	return res
	
try:
	formative = WordType.objects.get(name='Formative')
except WordType.DoesNotExist:
	formative = WordType(name='Formative')
	formative.save()
	
try:
	slot = Slot.objects.filter(word_type__name='Formative', number='IX').get(name='Ci+Vi')
except Slot.DoesNotExist:
	slot = Slot(number='IX', name='Ci+Vi', word_type=formative)
	slot.save()

for data in morph_dict:
	mood = value(data['mood'], 'Mood')
	ill = value(data['illocution'], 'Illocution')
	
	try:
		morph = Morpheme.objects.filter(slot__id=slot.id).get(content=data['slot'])
	except Morpheme.DoesNotExist:
		morph = Morpheme(content=data['slot'], slot=slot)
		morph.save()
		morph.values.add(mood)
		morph.values.add(ill)
		
	print(morph.id, ':', morph.content)
		
print('Done.')
