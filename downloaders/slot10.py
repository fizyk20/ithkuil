#!/usr/bin/env python
import http.client
from downloaders.table_parser import TableParser, reformat, replace_h
from morphology.models import *

sess = http.client.HTTPConnection('ithkuil.net', 80)

print('Downloading tables from ithkuil.net...')

sess.request('GET', '/03_morphology.html')
res = sess.getresponse()
html = res.read()

print('Downloaded.')
print('Parsing...')

parser = TableParser()
parser.feed(str(html))

def test_table(node):
	try:
		return node.tr[0].td[0].__data__ == 'ESSENCE & EXTENSION'
	except:
		return False
	
print('Parsed.')
print('Filtering for morphology tables...')

result2 = list(filter(test_table, parser.result))

print('Filtered.')
print('Reading data...')

def read_table(node):
	current_ess_ext = ''
	current_per = ''
	current_aff = ''
	configs = list(map(lambda x: reformat(x.__data__), node.tr[1].td))
	result = []
	for row_n in range(2, len(node.tr)):
		row = node.tr[row_n]
		mod_1 = 0
		mod_2 = 0
		if row_n == 2:
			mod_1 = 1
			current_ess_ext = reformat(row.td[0].__data__)
		if (row_n-2)%4 == 0:
			mod_2 = 1
			current_per = reformat(row.td[mod_1].__data__)
		current_aff = reformat(row.td[mod_1 + mod_2].__data__)
		for i in range(mod_1 + mod_2 + 1, len(row.td)):
			ess_ext = current_ess_ext.split('/')
			essence = ess_ext[0]
			extension = ess_ext[1]
			result.append({ 'essence': essence,
							'extension': extension,
							'perspective': current_per,
							'affiliation': current_aff,
							'configuration': configs[i - mod_1 - mod_2 - 1],
							'slot': replace_h(reformat(row.td[i].__data__)) })
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
	slot = Slot.objects.filter(word_type__name='Formative', number='X').get(name='Ca')
except Slot.DoesNotExist:
	slot = Slot(number='X', name='Ca', word_type=formative)
	slot.save()

i = 1
for data in morph_dict:
	essence = value(data['essence'], 'Essence')
	extension = value(data['extension'], 'Extension')
	perspective = value(data['perspective'], 'Perspective')
	affiliation = value(data['affiliation'], 'Affiliation')
	configuration = value(data['configuration'], 'Configuration')
	
	try:
		morph = Morpheme.objects.filter(slot__id=slot.id).get(content=data['slot'])
	except Morpheme.DoesNotExist:
		morph = Morpheme(content=data['slot'], slot=slot)
		morph.save()
		morph.values.add(essence)
		morph.values.add(extension)
		morph.values.add(perspective)
		morph.values.add(affiliation)
		morph.values.add(configuration)
		
	print('%d.' % i, morph.id, ':', morph.content, '-', essence.code, '/', extension.code, '/', perspective.code, '/', affiliation.code, '/', configuration.code)
	i += 1
		
print('Done.')
