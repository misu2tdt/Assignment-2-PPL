"""
AST Generation module for OPLang programming language.
This module contains the ASTGeneration class that converts parse trees
into Abstract Syntax Trees using the visitor pattern.
"""

from functools import reduce
from build.OPLangVisitor import OPLangVisitor
from build.OPLangParser import OPLangParser
from src.utils.nodes import *


class ASTGeneration(OPLangVisitor):

    # TODO // code các hàm từ build/OPLangParser.py
    pass
    # #! program: class_p+ EOF;
    # def visitProgram(self, ctx:OPLangParser.ProgramContext):
    #     return Program([self.visit(i) for i in ctx.class_p()])

    