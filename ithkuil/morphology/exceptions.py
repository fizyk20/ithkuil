class IthkuilException(Exception):
	msg = '%s'
	
	def __init__(self, val):
		self.val = val
		
	def __str__(self):
		return self.msg % self.val

class InvalidCharacter(IthkuilException):
	msg = 'Invalid character: %s'
	
class InvalidStress(IthkuilException):
	msg = 'Invalid stress on syllable: %s'
	
class AnalysisException(IthkuilException):
	msg = 'Word analysis error: %s'