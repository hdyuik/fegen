from common import Converter, EOF

from parser.lalr_dfa import LALRDFA
from parser.eq_symbols import LALRNFAEqualSymbols
from parser.channelling import Channelling
from parser.analyzer import LALRAnalyzer


class Parser:
    def __init__(self, grammar, key_func=None):
        self.grammar = grammar
        if key_func:
            self.key_func = lambda thing: thing if thing is EOF else key_func(thing)
        else:
            self.key_func = lambda thing: thing

        self.nfa = self.grammar.convert_to_nfa()
        Channelling().channelling(self.nfa, self.grammar)
        self.dfa = Converter().convert(self.nfa, LALRNFAEqualSymbols(self.nfa), LALRDFA)
        self.analyzer = LALRAnalyzer(self.dfa, self.key_func)

    def parse(self, sentence):
        sentence = list(sentence) + [EOF, ]
        children = self.analyzer.analyze(sentence)
        children.pop()
        return children[0]