#!/usr/bin/env python
import http.client
from table_parser import TableParser, reformat, replace_h

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
		return 'MOOD' in node.tr[0].td[2].__data__
	except:
		return False
	
print('Parsed.')
print('Filtering for morphology tables...')

result2 = list(filter(test_table, parser.result))

print('Filtered.')
print('Reading data...')

def read_table(node):
	result = []
	moods = ['FAC', 'SUB', 'ASM', 'SPC', 'COU', 'HYP', 'IPL', 'ASC']
	aspects = []
	for td in node.tr[1].td:
		if not 'ILLOCUTION' in td.__data__:
			moods.append(td.__data__.replace(' ',''))
			
	for i in range(2, len(node.tr)):
		aspect = node.tr[i].td[1].__data__ + '/'
		if aspect == 'none /':
			aspect = ''
		for j in range(3, len(node.tr[i].td)):
			mood = moods[j-3]
			data = node.tr[i].td[j].__data__.replace(' ','')
			data = replace_h(data)
			result.append(('%s%s'%(aspect, mood), data))
	return result

morph_dict = []
for node in result2:
	morph_dict += read_table(node)
	
print('Data read.')
print('Saving to slot3.dat...')

with open('../data/slot3.dat', 'a', encoding='utf-8') as f:
	for line in morph_dict:
		f.write('%s: %s\n' % line)
		
print('Done.')
