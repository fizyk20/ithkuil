from django.db import models

class Category(models.Model):
	'''Class representing a grammatical category'''
	name = models.CharField(max_length=128)
	description = models.TextField()
	
	def __unicode__(self):
		return self.name	
	def __str__(self):
		return self.name
	
class CategValue(models.Model):
	'''Class representing a value of a grammatical category'''
	code = models.CharField(max_length=8)
	name = models.CharField(max_length=128)
	description = models.TextField()
	
	category = models.ForeignKey(Category, related_name='values')
	
	def __unicode__(self):
		return '%s - %s' % (self.code, self.name)
	def __str__(self):
		return '%s - %s' % (self.code, self.name)
	
class WordType(models.Model):
	'''Class representing a type of a word'''
	name = models.CharField(max_length=128)
	description = models.TextField()
	regex = models.CharField(max_length=256)
	
	def __unicode__(self):
		return self.name
	def __str__(self):
		return self.name
	
class Slot(models.Model):
	'''Class representing a morphological slot in a word'''
	number = models.CharField(max_length=4)
	name = models.CharField(max_length=32)
	description = models.TextField()
	regex = models.CharField(max_length=64)
	
	word_type = models.ForeignKey(WordType)
	
	def __unicode__(self):
		return self.name
	def __str__(self):
		return self.name
	
class Morpheme(models.Model):
	'''Class representing a morpheme'''
	content = models.CharField(max_length=8)
	tone = models.CharField(max_length=16)
	stress = models.CharField(max_length=16)
	slot = models.ForeignKey(Slot)
	values = models.ManyToManyField(CategValue, related_name='morphemes')
	
	def __unicode__(self):
		return self.content
	def __str__(self):
		return self.content
	
