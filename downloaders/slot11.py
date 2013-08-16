#!/usr/bin/env python
import http.client
from downloaders.table_parser import TableParser, reformat, replace_h
from morphology.models import *

sess = http.client.HTTPConnection('ithkuil.net', 80)

print('Downloading tables from ithkuil.net...')

sess.request('GET', '/07_suffixes.html')
res = sess.getresponse()
html = res.read()

print('Downloaded.')
print('Parsing...')

parser = TableParser()
parser.feed(str(html))

def test_table(node):
	try:
		return reformat(node.tr[0].td[0].__data__)[0] == '-'
	except:
		return False
	
print('Parsed.')
print('Filtering for morphology tables...')

result2 = list(filter(test_table, parser.result))

print('Filtered.')
print('Reading data...')

def read_table(node):
	def res(row):
		result = []
		txt = row.td[0].__data__
		txt = txt.replace('-','')
		txt = txt.replace(' ','')
		pts = txt.split('/')
		for p in pts:
			result.append({'suffix': row.td[1].__data__, 'slot': p})
		return result
	
	result = res(node.tr[0])
	if node.tr[1].td[0].__data__[0] == '-':
		for row in node.tr:
			result = result + res(row)
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
	slot = Slot.objects.filter(word_type__name='Formative', number='XI').get(name='VxC')
except Slot.DoesNotExist:
	slot = Slot(number='XI', name='VxC', word_type=formative)
	slot.save()

for data in morph_dict:
	suf = value(data['suffix'], 'Suffix')
	
	try:
		morph = Morpheme.objects.filter(slot__id=slot.id).get(content=data['slot'])
	except Morpheme.DoesNotExist:
		morph = Morpheme(content=data['slot'], slot=slot)
		morph.save()
		morph.values.add(suf)
		print('Creating...')
		
	print(morph.id, ':', morph.content)
		
print('Done.')
