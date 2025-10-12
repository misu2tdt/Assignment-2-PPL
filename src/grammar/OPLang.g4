grammar OPLang;

@lexer::header {from lexererr import *}
@lexer::members {
def emit(self):
    tk = self.type
    if tk == self.UNCLOSE_STRING:
        result = super().emit(); raise UncloseString(result.text)
    elif tk == self.ILLEGAL_ESCAPE:
        result = super().emit(); raise IllegalEscape(result.text)
    elif tk == self.ERROR_CHAR:
        result = super().emit(); raise ErrorToken(result.text)
    else:
        return super().emit();
}
options { language=Python3; }


//PARSER


program: classDecl+ EOF;
classDecl: CLASS ID (EXTENDS ID)? LCURLY memberDecl* RCURLY;
memberDecl: attributeDecl | constructorDecl | destructorDecl | methodDecl;
methodDecl: STATIC? VOID ID {self._input.LA(1) == OPLangParser.LPAREN}? LPAREN param_list? RPAREN block_stmt
 | STATIC? typeRet AMP? ID {self._input.LA(1) == OPLangParser.LPAREN}? LPAREN param_list? RPAREN block_stmt;
attributeDecl: (STATIC | FINAL | STATIC FINAL | FINAL STATIC)? optype var_list SEMI;

optype: primitiveNonVoid | classType | arrayType;
primitiveNonVoid: INT | FLOAT | BOOLEAN | STRING;
classType: ID;
arrayType: (primitiveNonVoid | classType) LBRACK INTLIT RBRACK;

var_list: var (COMMA var)*;
var: ID (ASSIGN expression)? | AMP ID (ASSIGN expression)?;

typeRet: primitiveNonVoid | classType | arrayType;
param_list: param (SEMI param)*;
param: optype id_list | optype AMP id_list;
id_list: ID (COMMA ID)*;

constructorDecl: ID LPAREN param_list? RPAREN block_stmt;
destructorDecl: TILDE ID LPAREN RPAREN block_stmt;

statement: block_stmt | assign_stmt | if_stmt | for_stmt | break_stmt | continue_stmt | return_stmt | call_stmt;
block_stmt: LCURLY decl_part? stmt_part? RCURLY;
decl_part: localdecl+;
stmt_part: statement+;
localdecl: FINAL? optype var_list SEMI;
assign_stmt: lhs ASSIGN expression SEMI;

lhs
    : exprPrimary (LBRACK expression RBRACK)+
    | exprPrimary (LBRACK expression RBRACK)* (DOT ID (LPAREN argList? RPAREN)? )* DOT ID
    | ID
    ;

if_stmt: IF expression THEN statement (ELSE statement)?;
for_stmt: FOR ID ASSIGN expression (TO | DOWNTO) expression DO statement;
break_stmt: BREAK SEMI;
continue_stmt: CONTINUE SEMI;
return_stmt: RETURN expression SEMI;
call_stmt: exprDot DOT ID LPAREN argList? RPAREN SEMI;

expression: exprOr;
exprOr   : exprAnd (OR exprAnd)* ;
exprAnd  : exprRel (AND exprRel)* ;
exprRel  : exprEq ((LT | GT | LE | GE) exprEq)* ;
exprEq   : exprAdd ((EQUAL | NOT_EQUAL) exprAdd)? ;
exprAdd: exprMul ((ADD | SUB) exprMul)*;
exprMul: exprCat ((MUL | DIV | INTDIV | MOD) exprCat)*;
exprCat: exprUnary (CONCAT exprUnary)*;
exprUnary: NOT exprUnary | ADD exprUnary | SUB exprUnary | exprDot;
exprDot: exprPrimary (DOT ID (LPAREN argList? RPAREN)? | LBRACK expression RBRACK)*;
exprPrimary: NEW ID LPAREN argList? RPAREN | literal | THIS | NIL | ID | LPAREN expression RPAREN | arrayLiteral;

argList: expression (COMMA expression)*;

literal: INTLIT | FLOATLIT | STRINGLIT | TRUE | FALSE | NIL;
arrayLiteral: LCURLY literal (COMMA literal)* RCURLY;

//LEXER

BOOLEAN: 'boolean';
BREAK: 'break';
CLASS: 'class';
CONTINUE: 'continue';
DO: 'do';
ELSE: 'else';
EXTENDS: 'extends';
FLOAT: 'float';
IF: 'if';
INT: 'int';
NEW: 'new';
STRING: 'string';
THEN: 'then';
FOR: 'for';
RETURN: 'return';
TRUE: 'true';
FALSE: 'false';
VOID: 'void';
NIL: 'nil';
THIS: 'this';
FINAL: 'final';
STATIC: 'static';
TO: 'to';
DOWNTO: 'downto';

ASSIGN: ':=';
ADD: '+';
SUB: '-';
MUL: '*';
DIV: '/';
INTDIV: '\\';
MOD: '%';
EQUAL: '==';
NOT_EQUAL: '!=';
LE: '<=';
GE: '>=';
LT: '<';
GT: '>';
OR: '||';
AND: '&&';
NOT: '!';
CONCAT: '^';

LBRACK: '[';
RBRACK: ']';
LCURLY: '{';
RCURLY: '}';
LPAREN: '(';
RPAREN: ')';
SEMI: ';';
COLON: ':';
DOT: '.';
COMMA: ',';

TILDE: '~';
AMP: '&';

ID: [a-zA-Z_][a-zA-Z0-9_]*;
INTLIT: [0-9]+;
FLOATLIT: [0-9]+ '.' [0-9]* ([eE][+-]?[0-9]+)? | [0-9]+ [eE][+-]?[0-9]+;
STRINGLIT: '"' (ESC_SEQ | ~["\\\r\n])* '"' { self.text = self.text[1:-1] };
fragment ESC_SEQ: '\\' [bfrnt"\\];

BLOCK_COMMENT: '/*' .*? '*/' -> skip;
LINE_COMMENT: '#' ~[\r\n]* -> skip;
WS: [ \t\r\n\f]+ -> skip;

ILLEGAL_ESCAPE: '"' (ESC_SEQ | ~["\\\r\n])* '\\' ~[bfrnt"\\] { self.text = self.text[1:] };
UNCLOSE_STRING: '"' (ESC_SEQ | ~["\\\r\n])* ('\r\n' | '\n' | '\r') { self.text = self.text[1:] } | '"' (ESC_SEQ | ~["\\\r\n])* EOF { self.text = self.text[1:] };
ERROR_CHAR: .;
