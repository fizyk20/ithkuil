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
					result.append(('%s/%s'%(mood,ill), s))
	return result

morph_dict = []
for node in result2:
	morph_dict += read_table(node)
	
print('Data read.')
print('Saving to slot9.dat...')

with open('../data/slot9.dat', 'w', encoding='utf-8') as f:
	for line in morph_dict:
		f.write('%s: %s\n' % line)
		
print('Done.')
