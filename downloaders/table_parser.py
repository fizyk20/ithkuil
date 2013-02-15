import html.parser
from html.entities import name2codepoint
import re

class HTMLNode:

	def __init__(self, name, attrs, parent):
		self.name = name
		self.attrs = attrs
		self.parent = parent
		self.children = {}
		self.data = ''

	def __getitem__(self, item):
		if item == '__data__':
			return self.data
		else:
			try:
				return self.children[item]
			except:
				return None
				
	def __getattr__(self, attr):
		return self[attr]
		
	def addChild(self, child):
		tag = child.name
		if tag in self.children:
			self.children[tag].append(child)
		else:
			self.children[tag] = [child]

class TableParser(html.parser.HTMLParser):
	allowed_tags = ['table', 'tr', 'td']
	
	def __init__(self):
		super(TableParser, self).__init__()
		self.result = []
		self.currentNode = None
	
	def handle_starttag(self, tag, attrs):
		if tag not in self.allowed_tags:
			return None
		self.currentNode = HTMLNode(tag, attrs, self.currentNode)
		if not self.currentNode.parent:
			self.result.append(self.currentNode)
		else:
			self.currentNode.parent.addChild(self.currentNode)
			
	def handle_endtag(self, tag):
		if tag not in self.allowed_tags:
			return None
		if not self.currentNode or tag != self.currentNode.name:
			raise Exception('End tag not matching start tag!')
		self.currentNode = self.currentNode.parent
		
	def handle_data(self, data):
		if not self.currentNode:
			return None
		self.currentNode.data += data
		
	def handle_entityref(self, name):
		c = chr(name2codepoint[name])
		if self.currentNode:
			self.currentNode.data += c
		#print("Named ent:", c)

	def handle_charref(self, name):
		if name.startswith('x'):
			c = chr(int(name[1:], 16))
		else:
			c = chr(int(name))
		if self.currentNode:
			self.currentNode.data += c
		#print("Num ent  :", c)

def reformat(s):
	return s.replace(' ','').replace('\\n','').replace('+','/')

def replace_h(s):
	return re.sub('(ph|th|qh|kh|ch|čh)', lambda x: x.group(0)[0]+'ʰ', s)