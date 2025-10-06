import sys
import os
import subprocess

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "build"))

from antlr4 import *


from build.OPLangLexer import OPLangLexer
class Tokenizer:
    def __init__(self, input_string):
        self.input_stream = InputStream(input_string)
        self.lexer = OPLangLexer(self.input_stream)

    def get_tokens(self):
        tokens = []
        token = self.lexer.nextToken()
        while token.type != Token.EOF:
            tokens.append(token.text)
            try:
                token = self.lexer.nextToken()
            except Exception as e:
                tokens.append(str(e))
                return tokens
        return tokens + ["EOF"]

    def get_tokens_as_string(self):
        tokens = []
        try:
            while True:
                token = self.lexer.nextToken()
                if token.type == Token.EOF:
                    tokens.append("EOF")
                    break
                tokens.append(token.text)
        except Exception as e:
            if tokens:  # If we already have some tokens, append error
                tokens.append(str(e))
            else:  # If no tokens yet, just return error
                return str(e)
        return ",".join(tokens)

from build.OPLangParser import OPLangParser
from src.utils.error_listener import NewErrorListener
class Parser:
    def __init__(self, input_string):
        self.input_stream = InputStream(input_string)
        self.lexer = OPLangLexer(self.input_stream)
        self.token_stream = CommonTokenStream(self.lexer)
        self.parser = OPLangParser(self.token_stream)
        self.parser.removeErrorListeners()
        self.parser.addErrorListener(NewErrorListener.INSTANCE)

    def parse(self):
        try:
            self.parser.program()  # Assuming 'program' is the entry point of your grammar
            return "success"
        except Exception as e:
            return str(e)
        
from src.astgen.ast_generation import ASTGeneration
from src.utils.nodes import *
class ASTGenerator:
    """Class to generate AST from CS source code."""

    def __init__(self, input_string):
        self.input_string = input_string
        self.input_stream = InputStream(input_string)
        self.lexer = OPLangLexer(self.input_stream)
        self.token_stream = CommonTokenStream(self.lexer)
        self.parser = OPLangParser(self.token_stream)
        self.parser.removeErrorListeners()
        self.parser.addErrorListener(NewErrorListener.INSTANCE)
        self.ast_generator = ASTGeneration()

    def generate(self):
        """Generate AST from the input string."""
        try:
            parse_tree = self.parser.program() 
        except Exception as e:
            return "Parser " + str(e)
        
        # Generate AST using the visitor
        ast = self.ast_generator.visit(parse_tree)
        return ast
