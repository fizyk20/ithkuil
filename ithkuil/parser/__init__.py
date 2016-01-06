from arpeggio.peg import ParserPEG
from arpeggio import visit_parse_tree
from .grammar import grammar
from .visitor import FormativeVisitor

wordParser = ParserPEG(grammar, "word", debug=False)

def parseWord(word):
    return visit_parse_tree(wordParser.parse(word), FormativeVisitor(debug=False))