from ithkuil.parser.visitor import IthkuilVisitor
from ithkuil.parser import wordParser
from arpeggio import visit_parse_tree
from .formative import Formative
from .verbal import VerbalAdjunct
from .personal import PersonalAdjunct
from .affixual import AffixualAdjunct
from .aspectual import AspectualAdjunct
from .bias import BiasAdjunct
from ..helpers import handle_special_chars, filter_chars
import re

def remove_stress(txt):
    def remove_accents(m):
        s = m.group(0)
        return s.replace('á', 'a')\
                .replace('é', 'e')\
                .replace('í', 'i')\
                .replace('ó', 'o')\
                .replace('ú', 'u')\
                .replace('à', 'a')\
                .replace('è', 'e')\
                .replace('ò', 'o')\
                .replace('ì', 'i')\
                .replace('ù', 'u')

    stressed = {
        r'([ëöüâêîôû])\1': r'\1',
        'áu': 'au',
        'éu': 'eu',
        'íu': 'iu',
        'óu': 'ou',
        '[áéó]': remove_accents,
        '[àèò]': remove_accents,
        '([^aeiou]|^)[ìù]': remove_accents,
        '([^aeiou]|^)[íú]': remove_accents,
        '([aeou])í': r'\1ì',
        '([aeio])ú': r'\1ù'
    }

    for k, v in stressed.items():
        txt = re.sub(k, v, txt)

    return txt

class Factory(IthkuilVisitor):

    def visit_formative(self, node, children):
        result = super().visit_formative(node, children)
        return Formative(result)

    def visit_verbal_adjunct(self, node, children):
        result = super().visit_verbal_adjunct(node, children)
        return VerbalAdjunct(result)

    def visit_personal_adjunct(self, node, children):
        result = super().visit_personal_adjunct(node, children)
        return PersonalAdjunct(result)

    def visit_affixual_adjunct(self, node, children):
        result = super().visit_affixual_adjunct(node, children)
        return AffixualAdjunct(result)

    def visit_aspectual_adjunct(self, node, children):
        result = super().visit_aspectual_adjunct(node, children)
        return AspectualAdjunct(result)

    def visit_bias_adjunct(self, node, children):
        result = super().visit_bias_adjunct(node, children)
        return BiasAdjunct(result)

    def visit_vowels(self, node, children):
        '''This visiting function will remove stress marks from the vowels'''
        temp = ''.join(children)
        return remove_stress(temp)

    def visit_vz(self, node, children):
        temp = ''.join(children)
        return { 'Vz': remove_stress(temp) }

    def visit_vw(self, node, children):
        temp = ''.join(children)
        return { 'Vw': remove_stress(temp) }

    def visit_vcp(self, node, children):
        temp = ''.join(children)
        return remove_stress(temp)

    def visit_vf_format(self, node, children):
        temp = ''.join(children)
        return {'Vf': remove_stress(temp)}

    def visit_vf_no_format(self, node, children):
        temp = ''.join(children)
        return {'Vf': remove_stress(temp)}

    @classmethod
    def parseWord(cls, word):
        word = filter_chars(handle_special_chars(word.lower()))
        parse_tree = wordParser.parse(word)
        wordObj = visit_parse_tree(parse_tree, cls())
        wordObj.word = word
        return wordObj
