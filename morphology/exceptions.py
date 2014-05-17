class InvalidCharacter(Exception):
	
	def __init__(self, val):
		self.val = val
		
	def __str__(self):
		return 'Invalid character: %s' % self.val
	
class InvalidStress(Exception):
	
	def __init__(self, val):
		self.val = val
		
	def __str__(self):
		return 'Invalid stress on syllable: %s' % self.val