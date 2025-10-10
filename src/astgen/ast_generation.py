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
        base_type = self.visit(ctx.optype())
        has_ref = any(v.AMP() for v in ctx.var_list().var())
        attri_type = ReferenceType(base_type) if has_ref else base_type
        attris = []
        for v in ctx.var_list().var():
            name = v.ID().getText()
            init = self.visit(v.expression()) if v.expression() else None
            attris.append(Attribute(name, init))

        return AttributeDecl(is_static, is_final, attri_type, attris)

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
        return reduce(lambda a, b: a + b, [self.visit(p) for p in ctx.param()], [])

    # param: optype id_list | optype AMP id_list;
    def visitParam(self, ctx: OPLangParser.ParamContext):
        param_type = self.visit(ctx.optype())
        if ctx.AMP():
            param_type = ReferenceType(param_type)
        ids = [x.getText() for x in ctx.id_list().ID()]
        return [Parameter(param_type, id_name) for id_name in ids]


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

    # block_stmt: LCURLY decl_part? stmt_part? RCURLY;
    def visitBlock_stmt(self, ctx: OPLangParser.Block_stmtContext):
        decls = self.visit(ctx.decl_part()) if ctx.decl_part() else []
        stmts = self.visit(ctx.stmt_part()) if ctx.stmt_part() else []
        return BlockStatement(decls, stmts)

    # decl_part: localdecl+;
    def visitDecl_part(self, ctx: OPLangParser.Decl_partContext): 
        return [self.visit(x) for x in ctx.localdecl()]

    # stmt_part: statement+;
    def visitStmt_part(self, ctx: OPLangParser.Stmt_partContext): 
        return [self.visit(x) for x in ctx.statement()]

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

    # llhs
    #: exprPrimary (LBRACK expression RBRACK)+
    #| exprPrimary (LBRACK expression RBRACK)* (DOT ID (LPAREN argList? RPAREN)? )* DOT ID
    #| ID;
    def visitLhs(self, ctx: OPLangParser.LhsContext):
        if ctx.ID() and ctx.getChildCount() == 1:
            return IdLHS(ctx.ID(0).getText())
        base = self.visit(ctx.exprPrimary())
        bracket_ops = []
        for exp in ctx.expression():  
            bracket_ops.append(ArrayAccess(self.visit(exp)))

        node = PostfixExpression(base, bracket_ops) if bracket_ops else base
        i = 0
        consumed = 1  
        while consumed < ctx.getChildCount():
            if ctx.getChild(consumed).getText() == '[':
                consumed += 3
            else:
                break
        ops = []
        i = consumed
        n = ctx.getChildCount()
        while i < n:
            if ctx.getChild(i).getText() != '.':
                i += 1
                continue

            name = ctx.getChild(i + 1).getText()
            j = i + 2
            if j < n and ctx.getChild(j).getText() == '(':
                args = []
                if (j + 1) < n and isinstance(ctx.getChild(j + 1), OPLangParser.ArgListContext):
                    args = self.visit(ctx.getChild(j + 1))
                    j += 1
                ops.append(MethodCall(name, args))
                i = j + 2  
            else:
                ops.append(MemberAccess(name))
                i += 2

        if ops:
            # gộp với phần [] trước đó nếu có
            if isinstance(node, PostfixExpression):
                node = PostfixExpression(node.base, node.postfix_ops + ops)
            else:
                node = PostfixExpression(node, ops)

        # LHS là postfix hoặc id
        if isinstance(node, PostfixExpression):
            return PostfixLHS(node)
        if isinstance(node, Identifier):
            return IdLHS(node.name if hasattr(node, "name") else ctx.ID(0).getText())

        return PostfixLHS(node)

    # if_stmt: IF expression THEN statement (ELSE statement)?;
    def visitIf_stmt(self, ctx: OPLangParser.If_stmtContext): 
        if_part = self.visit(ctx.expression())
        then_part = self.visit(ctx.statement(0))
        else_part = self.visit(ctx.statement(1)) if ctx.statement(1) else None
        return IfStatement(if_part ,then_part, else_part)

    # for_stmt: FOR ID ASSIGN expression (TO / DOWNTO) expression DO statement;
    def visitFor_stmt(self, ctx: OPLangParser.For_stmtContext): 
        for_var = ctx.ID().getText()
        start_exp = self.visit(ctx.expression(0))
        end_exp = self.visit(ctx.expression(1))
        direction = ctx.getChild(4).getText()
        do_stmt = self.visit(ctx.statement())
        return ForStatement(for_var, start_exp, direction, end_exp, do_stmt)
    
    # break_stmt: BREAK SEMI;
    def visitBreak_stmt(self, ctx: OPLangParser.Break_stmtContext): 
        return BreakStatement()

    # continue_stmt: CONTINUE SEMI;
    def visitContinue_stmt(self, ctx: OPLangParser.Continue_stmtContext): 
        return ContinueStatement()

    # return_stmt: RETURN expression? SEMI;
    def visitReturn_stmt(self, ctx: OPLangParser.Return_stmtContext): 
        value = self.visit(ctx.expression()) if ctx.expression() else None
        return ReturnStatement(value)

    # call_stmt: (exprDot | ID) LPAREN argList? RPAREN SEMI;
    def visitCall_stmt(self, ctx: OPLangParser.Call_stmtContext):
        if ctx.exprDot():
            obj = self.visit(ctx.exprDot())
            method_name = ctx.ID().getText()
            args = self.visit(ctx.argList()) if ctx.argList() else []
            return MethodInvocationStatement(PostfixExpression(obj, [MethodCall(method_name, args)]))
        else:
            method_name = ctx.ID().getText()
            args = self.visit(ctx.argList()) if ctx.argList() else []
            return MethodInvocationStatement(PostfixExpression(Identifier(method_name), [MethodCall("", args)]))

    # expression: exprOr;
    def visitExpression(self, ctx: OPLangParser.ExpressionContext): 
        return self.visit(ctx.exprOr())

    # exprOr: exprAnd (OR exprAnd)*;
    def visitExprOr(self, ctx: OPLangParser.ExprOrContext): 
        left_side = self.visit(ctx.exprAnd(0))
        for i in range (1, len(ctx.exprAnd())):
            op = ctx.getChild(2 * i - 1).getText()
            right_side = self.visit(ctx.exprAnd(i))
            left_side = BinaryOp(left_side, op, right_side)
        return left_side

    # exprAnd: exprEq (AND exprEq)*;
    def visitExprAnd(self, ctx: OPLangParser.ExprAndContext): 
        left_side = self.visit(ctx.exprEq(0))
        for i in range (1, len(ctx.exprEq())):
            op = ctx.getChild(2 * i - 1).getText()
            right_side = self.visit(ctx.exprEq(i))
            left_side = BinaryOp(left_side, op, right_side)
        return left_side

    # exprEq: exprRel ((EQUAL | NOT_EQUAL) exprRel)?;
    def visitExprEq(self, ctx: OPLangParser.ExprEqContext):
        left_side = self.visit(ctx.exprRel(0))
        if ctx.EQUAL():
            op = ctx.EQUAL().getText()
            right_side = self.visit(ctx.exprRel(1))
            return BinaryOp(left_side, op, right_side)
        elif ctx.NOT_EQUAL():
            op = ctx.NOT_EQUAL().getText()
            right_side = self.visit(ctx.exprRel(1))
            return BinaryOp(left_side, op, right_side)
        else :
            return left_side

    # exprRel: exprAdd ((LT | LE | GT | GE) exprAdd)*;
    def visitExprRel(self, ctx: OPLangParser.ExprRelContext): 
        left_side = self.visit(ctx.exprAdd(0))
        for i in range (1, len(ctx.exprAdd())):
            if ctx.LT():
                op = ctx.LT(0).getText()
            elif ctx.LE():
                op = ctx.LE(0).getText()
            elif ctx.GT():
                op = ctx.GT(0).getText()
            else :
                op = ctx.GE(0).getText()
            right_side = self.visit(ctx.exprAdd(i))
            left_side = BinaryOp(left_side, op, right_side)
        return left_side
        

    # exprAdd: exprMul ((ADD | SUB | CONCAT) exprMul)*;
    def visitExprAdd(self, ctx: OPLangParser.ExprAddContext):
        left_side = self.visit(ctx.exprMul(0))
        for i in range(1, len(ctx.exprMul())):
            op = ctx.getChild(2 * i - 1).getText()
            right_side = self.visit(ctx.exprMul(i))
            left_side = BinaryOp(left_side, op, right_side)
        return left_side

    # exprMul: exprUnary ((MUL | DIV | INTDIV | MOD) exprUnary)*;
    def visitExprMul(self, ctx: OPLangParser.ExprMulContext):
        left_side = self.visit(ctx.exprUnary(0))
        for i in range(1, len(ctx.exprUnary())):
            op = ctx.getChild(2 * i - 1).getText()
            right_side = self.visit(ctx.exprUnary(i))
            left_side = BinaryOp(left_side, op, right_side)
        return left_side
        

    # exprUnary: NOT exprUnary | ADD exprUnary | SUB exprUnary | exprDot;
    def visitExprUnary(self, ctx: OPLangParser.ExprUnaryContext): 
        if ctx.NOT():
            op = ctx.NOT().getText()
            return UnaryOp(op, self.visit(ctx.exprUnary()))
        elif ctx.ADD():
            op = ctx.ADD().getText()
            return UnaryOp(op, self.visit(ctx.exprUnary()))
        elif ctx.SUB():
            op = ctx.SUB().getText()
            return UnaryOp(op, self.visit(ctx.exprUnary()))
        else:
            return self.visit(ctx.exprDot())

    # exprDot: exprIndex ( {self._input.LA(1) == OPLangParser.DOT}? DOT ID (LPAREN argList? RPAREN)? )*;
    def visitExprDot(self, ctx: OPLangParser.ExprDotContext): 
        base = self.visit(ctx.exprPrimary())
        postfix_ops = []

        i = 1
        n = ctx.getChildCount()
        while i < n:
            tok = ctx.getChild(i).getText()

            if tok == '.':
                name = ctx.getChild(i + 1).getText()
                # .ID(...)
                if (i + 2) < n and ctx.getChild(i + 2).getText() == '(':
                    args = []
                    if (i + 3) < n and isinstance(ctx.getChild(i + 3), OPLangParser.ArgListContext):
                        args = self.visit(ctx.getChild(i + 3))
                        i += 1  # skip argList
                    postfix_ops.append(MethodCall(name, args))
                    i += 4  # skip ". ID ( ... )"
                else:
                    # .ID
                    postfix_ops.append(MemberAccess(name))
                    i += 2

            elif tok == '[':
                # [ expression ]
                exp_ctx = ctx.getChild(i + 1)
                postfix_ops.append(ArrayAccess(self.visit(exp_ctx)))
                i += 3
            else:
                i += 1

        if not postfix_ops:
            return base
        if isinstance(base, PostfixExpression):
            return PostfixExpression(base.base, base.postfix_ops + postfix_ops)
        return PostfixExpression(base, postfix_ops)


    # exprPrimary: NEW ID LPAREN argList? RPAREN | literal | THIS | NIL | ID | LPAREN expression RPAREN | arrayLiteral;
    def visitExprPrimary(self, ctx: OPLangParser.ExprPrimaryContext): 
        if ctx.NEW():
            class_name = ctx.ID().getText()
            args = self.visit(ctx.argList()) if ctx.argList() else []
            return ObjectCreation(class_name, args)
        elif ctx.literal():
            return self.visit(ctx.literal())
        elif ctx.THIS():
            return ThisExpression()
        elif ctx.NIL():
            return NilLiteral()
        elif ctx.ID():
            return Identifier(ctx.ID().getText())
        elif ctx.expression():
            return ParenthesizedExpression(self.visit(ctx.expression()))
        else:
            return self.visit(ctx.arrayLiteral())

    # argList: expression (COMMA expression)*;
    def visitArgList(self, ctx: OPLangParser.ArgListContext): 
        return [self.visit(expr) for expr in ctx.expression()]

    # literal: INTLIT | FLOATLIT | STRINGLIT | TRUE | FALSE | NIL;
    def visitLiteral(self, ctx: OPLangParser.LiteralContext): 
        if ctx.INTLIT():
            return IntLiteral(int(ctx.INTLIT().getText()))
        elif ctx.FLOATLIT():
            return FloatLiteral(float(ctx.FLOATLIT().getText()))
        elif ctx.STRINGLIT():
            return StringLiteral(ctx.STRINGLIT().getText())
        elif ctx.TRUE():
            return BoolLiteral(True)
        elif ctx.FALSE():
            return BoolLiteral(False)
        else:
            return NilLiteral()

    # arrayLiteral: LCURLY literal (COMMA literal)* RCURLY;
    def visitArrayLiteral(self, ctx: OPLangParser.ArrayLiteralContext): 
        elements = [self.visit(lit) for lit in ctx.literal()]
        return ArrayLiteral(elements)



    