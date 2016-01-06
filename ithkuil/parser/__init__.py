from arpeggio.peg import ParserPEG
from arpeggio import visit_parse_tree
from .grammar import grammar
from .visitor import IthkuilVisitor

wordParser = ParserPEG(grammar, "word", debug=False)

def parseWord(word):
    return visit_parse_tree(wordParser.parse(word), IthkuilVisitor(debug=False))