#!/usr/bin/env python
import http.client
from table_parser import TableParser, reformat, replace_h

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
			name = '%s/%s/%s/%s' % (current_ess_ext, current_per, current_aff, configs[i - mod_1 - mod_2 - 1])
			result.append((name, replace_h(reformat(row.td[i].__data__))))
	return result

morph_dict = []
for node in result2:
	morph_dict += read_table(node)
	
print('Data read.')
print('Saving to slot10.dat...')

with open('../data/slot10.dat', 'w', encoding='utf-8') as f:
	for line in morph_dict:
		f.write('%s: %s\n' % line)
		
print('Done.')
