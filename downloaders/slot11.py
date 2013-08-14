#!/usr/bin/env python
import http.client
from table_parser import TableParser, reformat, replace_h

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
		return node.tr[0].td[0].__data__[0] == '-'
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
			result.append((row.td[1].__data__, p))
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
print('Saving to slot11.dat...')

with open('../data/slot11.dat', 'w', encoding='utf-8') as f:
	for line in morph_dict:
		f.write('%s: %s\n' % line)
		
print('Done.')
