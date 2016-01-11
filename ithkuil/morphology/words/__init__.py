from ithkuil.parser.visitor import IthkuilVisitor, CombineVisitor
from ithkuil.parser import wordParser
from arpeggio import visit_parse_tree
from .formative import Formative
from .verbal import VerbalAdjunct
from .personal import PersonalAdjunct
from .affixual import AffixualAdjunct
from .aspectual import AspectualAdjunct
from .bias import BiasAdjunct
from ..helpers import handle_special_chars, filter_chars

class Factory(IthkuilVisitor):
    
    def visit_formative(self, node, children):
        word = visit_parse_tree(node, CombineVisitor())
        result = super().visit_formative(node, children)
        return Formative(word, result)
    
    def visit_verbal_adjunct(self, node, children):
        word = visit_parse_tree(node, CombineVisitor())
        result = super().visit_formative(node, children)
        return Formative(word, result)
    
    def visit_personal_adjunct(self, node, children):
        word = visit_parse_tree(node, CombineVisitor())
        result = super().visit_formative(node, children)
        return Formative(word, result)
    
    def visit_affixual_adjunct(self, node, children):
        word = visit_parse_tree(node, CombineVisitor())
        result = super().visit_formative(node, children)
        return Formative(word, result)
    
    def visit_aspectual_adjunct(self, node, children):
        word = visit_parse_tree(node, CombineVisitor())
        result = super().visit_formative(node, children)
        return Formative(word, result)
    
    def visit_bias_adjunct(self, node, children):
        word = visit_parse_tree(node, CombineVisitor())
        result = super().visit_formative(node, children)
        return Formative(word, result)
    
    @classmethod
    def parseWord(cls, word):
        word = filter_chars(handle_special_chars(word.lower()))
        parse_tree = wordParser.parse(word)
        return visit_parse_tree(parse_tree, cls())
        