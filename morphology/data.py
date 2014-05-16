from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship, backref

__all__ = ['ithCategory', 'ithCategValue', 'ithWordType', 'ithSlot', 'ithMorpheme']

Base = declarative_base()

class ithCategory(Base):
	'''Class representing a grammatical category'''
	__tablename__ = 'ith_category'
	
	id = Column(Integer, primary_key=True)
	name = Column(String(128))
	description = Column(Text)
	

class ithCategValue(Base):
	'''Class representing a value of a grammatical category'''
	__tablename__ = 'ith_categvalue'
	
	id = Column(Integer, primary_key=True)
	code = Column(String(8))
	name = Column(String(128))
	description = Column(Text)
	

class ithWordType(Base):
	'''Class representing a type of a word'''
	__tablename__ = 'ith_wordtype'
	
	id = Column(Integer, primary_key=True)
	name = Column(String(128))
	description = Column(Text)
	regex = Column(String(256))
	

class ithSlot(Base):
	'''Class representing a morphological slot in a word'''
	__tablename__ = 'ith_slot'
	
	id = Column(Integer, primary_key=True)
	number = Column(String(4))
	name = Column(String(32))
	description = Column(Text)
	regex = Column(String(64))
	
	word_type_id = Column(Integer, ForeignKey('ith_wordtype.id'))
	word_type = relationship('ithWordType', backref=backref('slots', order_by=id))
	

morpheme_values = Table('ith_morpheme_values', Base.metadata,
					Column('morpheme_id', Integer, ForeignKey('ith_morpheme.id')),
					Column('categvalue_id', Integer, ForeignKey('ith_categvalue.id')))
	

class ithMorpheme(Base):
	'''Class representing a morpheme'''
	__tablename__ = 'ith_morpheme'
	
	id = Column(Integer, primary_key=True)
	content = Column(String(8))
	tone = Column(String(16))
	stress = Column(String(16))
	slot_id = Column(Integer, ForeignKey('ith_slot.id'))
	slot = relationship('ithSlot', backref=backref('morphemes', order_by=id))
	values = relationship('ithCategValue', secondary=morpheme_values, backref='morphemes')
	