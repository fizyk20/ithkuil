#!/usr/bin/env python
import http.client
from downloaders.table_parser import TableParser, reformat, replace_h
from morphology.models import *

sess = http.client.HTTPConnection('ithkuil.net', 80)

print('Downloading tables from ithkuil.net...')

sess.request('GET', '/04_case.html')
res = sess.getresponse()
html = res.read()

sess.request('GET', '/06_verbs_2.html')
res = sess.getresponse()
html2 = res.read()

print('Downloaded.')
print('Parsing...')

parser = TableParser()
parser.feed(str(html))
parser.feed(str(html2))

def test_table(node):
	try:
		return node.tr[0].td[0].__data__ in ['1 OBL', 'Mutation Series ']
	except:
		return False
	
print('Parsed.')
print('Filtering for morphology tables...')

result2 = list(filter(test_table, parser.result))

print('Filtered.')
print('Reading data...')

def read_table(node):
	result = []
	if node.tr[0].td[0].__data__ == '1 OBL':
		for i in range(len(node.tr)):
			for j in range(0, len(node.tr[i].td), 2):
				case = node.tr[i].td[j].__data__.split()[1]
				case = case.replace('*','')
				slots = node.tr[i].td[j+1].__data__.split('/')
				slots = list(map(lambda x: x.replace(' ',''), slots))
				for s in slots:
					result.append({'case':case, 'slot':s})
	else:
		for i in range(len(node.tr)):
			case = node.tr[i].td[1].__data__
			slots = node.tr[i].td[3].__data__.split('/')
			slots = list(map(lambda x: x.replace(' ',''), slots))
			for s in slots:
				result.append({'case':case, 'slot':s})
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
	slot = Slot.objects.filter(word_type__name='Formative', number='VIII').get(name='Vc')
except Slot.DoesNotExist:
	slot = Slot(number='VIII', name='Vc', word_type=formative)
	slot.save()

for data in morph_dict:
	case = value(data['case'], 'Case')
	
	try:
		morph = Morpheme.objects.filter(slot__id=slot.id).get(content=data['slot'])
	except Morpheme.DoesNotExist:
		morph = Morpheme(content=data['slot'], slot=slot)
		morph.save()
		morph.values.add(case)
		
	print(morph.id, ':', morph.content)
		
print('Done.')
