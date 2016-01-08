from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

__all__ = ['ithCategory', 'ithCategValue', 'ithWordType', 'ithSlot', 'ithMorpheme', 'ithMorphemeSlot']

Base = declarative_base()

class ithWordType(Base):
    '''Class representing a type of a word'''
    __tablename__ = 'ith_wordtype'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    description = Column(Text)

wordtypes_categories = Table('ith_wordtype_category', Base.metadata,
                        Column('wordtype_id', Integer, ForeignKey('ith_wordtype.id')),
                        Column('category_id', Integer, ForeignKey('ith_category.id')))

class ithCategory(Base):
    '''Class representing a grammatical category'''
    __tablename__ = 'ith_category'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    description = Column(Text)
    word_types = relationship('ithWordType', secondary=wordtypes_categories, backref='categories')

class ithSlot(Base):
    '''Class representing a morphological slot in a word'''
    __tablename__ = 'ith_slot'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(8))
    description = Column(Text)
    
    wordtype_id = Column(Integer, ForeignKey('ith_wordtype.id'))
    wordtype = relationship('ithWordType', backref='slots')

class ithMorpheme(Base):
    '''Class representing a morpheme'''
    __tablename__ = 'ith_morpheme'
    
    id = Column(Integer, primary_key=True)
    morpheme = Column(String(8))

class ithMorphemeSlot(Base):
    __tablename__ = 'ith_morpheme_slot'

    id = Column(Integer, primary_key=True)
    morpheme_id = Column(Integer, ForeignKey('ith_morpheme.id'))
    slot_id = Column(Integer, ForeignKey('ith_slot.id'))

    morpheme = relationship('ithMorpheme', backref='slots')
    slot = relationship('ithSlot', backref='morphemes')
    

morpheme_slots_values = Table('ith_morpheme_slots_values', Base.metadata,
                        Column('morpheme_slot_id', Integer, ForeignKey('ith_morpheme_slot.id')),
                        Column('categvalue_id', Integer, ForeignKey('ith_categvalue.id')))
    

class ithCategValue(Base):
    '''Class representing a value of a grammatical category'''
    __tablename__ = 'ith_categvalue'
    
    id = Column(Integer, primary_key=True)
    code = Column(String(8))
    name = Column(String(128))
    description = Column(Text)
    category_id = Column(Integer, ForeignKey('ith_category.id'))
    category = relationship('ithCategory')
    morpheme_slots = relationship('ithMorphemeSlot', secondary=morpheme_slots_values, backref='values')
