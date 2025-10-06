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

    # program: classDecl+ EOF;
    def visitProgram(self, ctx: OPLangParser.ProgramContext): 
        class_decls = [self.visit(x) for x in ctx.classDecl()]
        return Program(class_decls)

    # classDecl: CLASS ID (EXTENDS ID)? LCURLY memberDecl* RCURLY;
    def visitClassDecl(self, ctx: OPLangParser.ClassDeclContext):
        name = ctx.ID(0).getText()
        super_class = ctx.ID(1).getText() if ctx.EXTENDS() else None
        members = [self.visit(x) for x in ctx.memberDecl()]
        return ClassDecl(name, super_class, members)

    # memberDecl: attributeDecl | constructorDecl | destructorDecl | methodDecl;
    def visitMemberDecl(self, ctx: OPLangParser.MemberDeclContext): 
        if ctx.attributeDecl():
            return self.visit(ctx.attributeDecl())
        elif ctx.constructorDecl():
            return self.visit(ctx.constructorDecl())
        elif ctx.destructorDecl():
            return self.visit(ctx.destructorDecl())
        else :
            return self.visit(ctx.methodDecl())

    # methodDecl: STATIC? VOID ID LPAREN param_list? RPAREN block_stmt
    #            |STATIC? typeRet AMP? ID LPAREN param_list? RPAREN block_stmt;
    def visitMethodDecl(self, ctx: OPLangParser.MethodDeclContext):
        is_static = bool(ctx.STATIC())
        if ctx.VOID():
            name = ctx.ID().getText()
            ret_type = PrimitiveType("void")
            param = self.visit(ctx.param_list()) if ctx.param_list() else []
            body = self.visit(ctx.block_stmt())
            return MethodDecl(is_static, ret_type, name, param, body)
        else :
            name = ctx.ID().getText()
            ret_type = self.visit(ctx.typeRet())
            param = self.visit(ctx.param_list()) if ctx.param_list() else []
            body = self.visit(ctx.block_stmt())
            return MethodDecl(is_static, ret_type, name, param, body)

    # attributeDecl: (STATIC | FINAL | STATIC FINAL | FINAL STATIC)? optype var_list SEMI;
    def visitAttributeDecl(self, ctx: OPLangParser.AttributeDeclContext): 
        is_static = bool(ctx.STATIC())
        is_final = bool(ctx.FINAL())
        typee = self.visit(ctx.optype())
        var_list = self.visit(ctx.var_list())
        return AttributeDecl(is_static, is_final, typee, var_list)

    # optype: primitiveNonVoid | classType | arrayType;
    def visitOptype(self, ctx: OPLangParser.OptypeContext): 
        if ctx.primitiveNonVoid():
            return self.visit(ctx.primitiveNonVoid())
        elif ctx.classType():
            return self.visit(ctx.classType())
        else:
            return self.visit(ctx.arrayType())

    # primitiveNonVoid: INT | FLOAT | BOOLEAN | STRING;
    def visitPrimitiveNonVoid(self, ctx: OPLangParser.PrimitiveNonVoidContext): 
        if ctx.INT():
            return PrimitiveType("int")
        elif ctx.FLOAT():
            return PrimitiveType("float")
        elif ctx.BOOLEAN():
            return PrimitiveType("boolean")
        else :
            return PrimitiveType("string")

    # classType: ID;
    def visitClassType(self, ctx: OPLangParser.ClassTypeContext): 
        return ClassType(ctx.ID().getText())

    # arrayType: (primitiveNonVoid | classType) LBRACK INTLIT RBRACK;
    def visitArrayType(self, ctx: OPLangParser.ArrayTypeContext):
        size = int(ctx.INTLIT().getText())
        if ctx.classType():
            ele_type = self.visit(ctx.classType())
            return ArrayType(ele_type, size)
        else :
            ele_type = self.visit(ctx.primitiveNonVoid())
            return ArrayType(ele_type, size)
            

    # var_list: var (COMMA var)*;
    def visitVar_list(self, ctx: OPLangParser.Var_listContext): 
        return [self.visit(x) for x in ctx.var()]

    # var: ID (ASSIGN expression)? | AMP ID (ASSIGN expression)?;
    def visitVar(self, ctx: OPLangParser.VarContext):
        name = ctx.ID().getText()
        init = self.visit(ctx.expression()) if ctx.expression() else None
        return Variable(name, init)

    # typeRet: primitiveNonVoid | classType | arrayType;
    def visitTypeRet(self, ctx: OPLangParser.TypeRetContext):
        if ctx.primitiveNonVoid():
            return self.visit(ctx.primitiveNonVoid())
        elif ctx.classType():
            return self.visit(ctx.classType())
        else: 
            return self.visit(ctx.arrayType())


    # param_list: param (SEMI param)*;
    def visitParam_list(self, ctx: OPLangParser.Param_listContext): 
        return [self.visit(x) for x in ctx.param()]

    # param: optype id_list | optype AMP id_list;
    def visitParam(self, ctx: OPLangParser.ParamContext):
        param_type = self.visit(ctx.optype())
        name = self.visit(ctx.id_list())
        return Parameter(param_type, name)

    # id_list: ID (COMMA ID)*;
    def visitId_list(self, ctx: OPLangParser.Id_listContext): 
        return [x.getText() for x in ctx.ID()]

    # constructorDecl: ID LPAREN param_list? RPAREN block_stmt;
    def visitConstructorDecl(self, ctx: OPLangParser.ConstructorDeclContext): 
        name = ctx.ID().getText()
        param = self.visit(ctx.param_list()) if ctx.param_list() else []
        body = self.visit(ctx.block_stmt())
        return ConstructorDecl(name, param, body)

    # destructorDecl: TILDE ID LPAREN RPAREN block_stmt;
    def visitDestructorDecl(self, ctx: OPLangParser.DestructorDeclContext): 
        name = ctx.ID().getText()
        body = self.visit(ctx.block_stmt())
        return DestructorDecl(name, body)

    # statement: assign_stmt | if_stmt | for_stmt | break_stmt | continue_stmt | return_stmt | call_stmt | block_stmt;
    def visitStatement(self, ctx: OPLangParser.StatementContext): 
        if ctx.assign_stmt():
            return self.visit(ctx.assign_stmt())
        elif ctx.if_stmt():
            return self.visit(ctx.if_stmt())
        elif ctx.for_stmt():
            return self.visit(ctx.for_stmt())
        elif ctx.break_stmt():
            return self.visit(ctx.break_stmt())
        elif ctx.continue_stmt():
            return self.visit(ctx.continue_stmt())
        elif ctx.return_stmt():
            return self.visit(ctx.return_stmt())
        elif ctx.call_stmt():
            return self.visit(ctx.call_stmt())
        else :
            return self.visit(ctx.block_stmt())

    # block_stmt: LCURLY decl_part* stmt_part* RCURLY;
    def visitBlock_stmt(self, ctx: OPLangParser.Block_stmtContext): 
        decl_part = [self.visit(x) for x in ctx.decl_part()] if ctx.decl_part else []
        stmt_part = [self.visit(y) for y in ctx.stmt_part()] if ctx.stmt_part else []
        return BlockStatement(decl_part, stmt_part)

    # decl_part: localdecl;
    def visitDecl_part(self, ctx: OPLangParser.Decl_partContext): 
        return self.visit(ctx.localdecl())

    # stmt_part: statement;
    def visitStmt_part(self, ctx: OPLangParser.Stmt_partContext): 
        return self.visit(ctx.statement())

    # localdecl: FINAL? optype var_list SEMI;
    def visitLocaldecl(self, ctx: OPLangParser.LocaldeclContext): 
        is_final = bool(ctx.FINAL())
        typee = self.visit(ctx.optype())
        name = self.visit(ctx.var_list())
        return VariableDecl(is_final, typee, name)

    # assign_stmt: lhs ASSIGN expression SEMI;
    def visitAssign_stmt(self, ctx: OPLangParser.Assign_stmtContext):
        left_side = self.visit(ctx.lhs())
        right_side = self.visit(ctx.expression())
        return AssignmentStatement(left_side, right_side)

    # lhs: exprPrimary (LBRACK expression RBRACK)+
    #| exprIndex (DOT ID (LPAREN argList? RPAREN)?)* DOT ID
    #| ID ;
    def visitLhs(self, ctx: OPLangParser.LhsContext):
        if ctx.getChildCount() == 3:
            iden = IdLHS(ctx.ID().getText())
            index = ArrayAccess(ctx.expression())
            return PostfixLHS(iden, index)
        elif ctx.ID():
            return IdLHS(ctx.ID().getText())
        else :
            return self.visit(ctx.expreDot())

    # if_stmt: IF expression THEN statement (ELSE statement)?;
    def visitIf_stmt(self, ctx: OPLangParser.If_stmtContext): ...

    # for_stmt: FOR ID ASSIGN expression TO expression DO statement;
    def visitFor_stmt(self, ctx: OPLangParser.For_stmtContext): ...

    # break_stmt: BREAK SEMI;
    def visitBreak_stmt(self, ctx: OPLangParser.Break_stmtContext): ...

    # continue_stmt: CONTINUE SEMI;
    def visitContinue_stmt(self, ctx: OPLangParser.Continue_stmtContext): ...

    # return_stmt: RETURN expression? SEMI;
    def visitReturn_stmt(self, ctx: OPLangParser.Return_stmtContext): ...

    # call_stmt: (exprDot | ID) LPAREN argList? RPAREN SEMI;
    def visitCall_stmt(self, ctx: OPLangParser.Call_stmtContext): ...

        # expression: exprOr;
    def visitExpression(self, ctx: OPLangParser.ExpressionContext): ...

    # exprOr: exprAnd (OR exprAnd)*;
    def visitExprOr(self, ctx: OPLangParser.ExprOrContext): ...

    # exprAnd: exprEq (AND exprEq)*;
    def visitExprAnd(self, ctx: OPLangParser.ExprAndContext): ...

    # exprEq: exprRel ((EQ | NEQ) exprRel)*;
    def visitExprEq(self, ctx: OPLangParser.ExprEqContext): ...

    # exprRel: exprAdd ((LT | LE | GT | GE) exprAdd)?;
    def visitExprRel(self, ctx: OPLangParser.ExprRelContext): ...

    # exprAdd: exprMul ((PLUS | MINUS) exprMul)*;
    def visitExprAdd(self, ctx: OPLangParser.ExprAddContext): ...

    # exprMul: exprUnary ((MUL | DIV | MOD) exprUnary)*;
    def visitExprMul(self, ctx: OPLangParser.ExprMulContext): ...

    # exprUnary: (NOT | MINUS) exprUnary | exprDot;
    def visitExprUnary(self, ctx: OPLangParser.ExprUnaryContext): ...

    # exprDot: exprPrimary (DOT ID (LPAREN argList? RPAREN)?)?;
    def visitExprDot(self, ctx: OPLangParser.ExprDotContext): ...

    # exprIndex: exprPrimary LBRACK expression RBRACK;
    def visitExprIndex(self, ctx: OPLangParser.ExprIndexContext): ...

    # exprPrimary: literal | ID | THIS | (LPAREN expression RPAREN);
    def visitExprPrimary(self, ctx: OPLangParser.ExprPrimaryContext): ...

    # argList: expression (COMMA expression)*;
    def visitArgList(self, ctx: OPLangParser.ArgListContext): ...

    # literal: INTLIT | FLOATLIT | STRINGLIT | BOOLEANLIT | arrayLiteral;
    def visitLiteral(self, ctx: OPLangParser.LiteralContext): ...

    # arrayLiteral: LBRACK (literal (COMMA literal)*)? RBRACK;
    def visitArrayLiteral(self, ctx: OPLangParser.ArrayLiteralContext): ...


    