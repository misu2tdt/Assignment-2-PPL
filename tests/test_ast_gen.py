
from utils import ASTGenerator
from src.utils.nodes import *

def test_001():
    """Test basic class declaration AST generation"""
    source = """class TestClass {
        int x;
    }"""
    expected = "Program([ClassDecl(TestClass, [AttributeDecl(PrimitiveType(int), [Attribute(x)])])])"
    # Just check that it doesn't return an error
    assert str(ASTGenerator(source).generate()) == expected


def test_002():
    """Test class with method declaration AST generation"""
    source = """class TestClass {
        void main() {
        }
    }"""
    expected = "Program([ClassDecl(TestClass, [MethodDecl(PrimitiveType(void) main([]), BlockStatement(stmts=[]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_003():
    """Test class with constructor AST generation"""
    source = """class TestClass {
        int x;
        TestClass(int x) {
            this.x := x;
        }
    }"""
    expected = "Program([ClassDecl(TestClass, [AttributeDecl(PrimitiveType(int), [Attribute(x)]), ConstructorDecl(TestClass([Parameter(PrimitiveType(int) x)]), BlockStatement(stmts=[AssignmentStatement(PostfixLHS(PostfixExpression(ThisExpression(this).x)) := Identifier(x))]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_004():
    """Test class with inheritance AST generation"""
    source = """class Child extends Parent {
        int y;
    }"""
    expected = "Program([ClassDecl(Child, extends Parent, [AttributeDecl(PrimitiveType(int), [Attribute(y)])])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_005():
    """Test static and final attributes AST generation"""
    source = """class TestClass {
        static final int MAX_SIZE := 100;
        final float PI := 3.14;
    }"""
    expected = "Program([ClassDecl(TestClass, [AttributeDecl(static final PrimitiveType(int), [Attribute(MAX_SIZE = IntLiteral(100))]), AttributeDecl(final PrimitiveType(float), [Attribute(PI = FloatLiteral(3.14))])])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_006():
    """Test if-else statement AST generation"""
    source = """class TestClass {
        void main() {
            if x > 0 then {
                return x;
            } else {
                return 0;
            }
        }
    }"""
    expected = "Program([ClassDecl(TestClass, [MethodDecl(PrimitiveType(void) main([]), BlockStatement(stmts=[IfStatement(if BinaryOp(Identifier(x), >, IntLiteral(0)) then BlockStatement(stmts=[ReturnStatement(return Identifier(x))]), else BlockStatement(stmts=[ReturnStatement(return IntLiteral(0))]))]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_007():
    """Test for loop AST generation"""
    source = """class TestClass {
        void main() {
            int sum := 0;
            for i := 1 to 10 do {
                sum := sum + i;
            }
        }
    }"""
    expected = "Program([ClassDecl(TestClass, [MethodDecl(PrimitiveType(void) main([]), BlockStatement(vars=[VariableDecl(PrimitiveType(int), [Variable(sum = IntLiteral(0))])], stmts=[ForStatement(for i := IntLiteral(1) to IntLiteral(10) do BlockStatement(stmts=[AssignmentStatement(IdLHS(sum) := BinaryOp(Identifier(sum), +, Identifier(i)))]))]))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_008():
    """Test array operations AST generation"""
    source = """class TestClass {
        void main() {
            int[5] arr;
            arr[0] := 42;
        }
    }"""
    expected = "Program([ClassDecl(TestClass, [MethodDecl(PrimitiveType(void) main([]), BlockStatement(vars=[VariableDecl(ArrayType(PrimitiveType(int)[5]), [Variable(arr)])], stmts=[AssignmentStatement(PostfixLHS(PostfixExpression(Identifier(arr)[IntLiteral(0)])) := IntLiteral(42))]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_009():
    """Test object creation and method call AST generation"""
    source = """class TestClass {
        void main() {
            Rectangle r := new Rectangle(5.0, 3.0);
            float area := r.getArea();
        }
    }"""
    expected = "Program([ClassDecl(TestClass, [MethodDecl(PrimitiveType(void) main([]), BlockStatement(vars=[VariableDecl(ClassType(Rectangle), [Variable(r = ObjectCreation(new Rectangle(FloatLiteral(5.0), FloatLiteral(3.0))))]), VariableDecl(PrimitiveType(float), [Variable(area = PostfixExpression(Identifier(r).getArea()))])], stmts=[]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_010():
    """Test reference type AST generation"""
    source = """class TestClass {
        void swap(int & a; int & b) {
            int temp := a;
            a := b;
            b := temp;
        }
    }"""
    expected = "Program([ClassDecl(TestClass, [MethodDecl(PrimitiveType(void) swap([Parameter(ReferenceType(PrimitiveType(int) &) a), Parameter(ReferenceType(PrimitiveType(int) &) b)]), BlockStatement(vars=[VariableDecl(PrimitiveType(int), [Variable(temp = Identifier(a))])], stmts=[AssignmentStatement(IdLHS(a) := Identifier(b)), AssignmentStatement(IdLHS(b) := Identifier(temp))]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_011():
    """Test destructor AST generation"""
    source = """class TestClass {
        ~TestClass() {
            int x := 0;
        }
    }"""
    expected = "Program([ClassDecl(TestClass, [DestructorDecl(~TestClass(), BlockStatement(vars=[VariableDecl(PrimitiveType(int), [Variable(x = IntLiteral(0))])], stmts=[]))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_015():
    source = """
        class V {
            final int a;
            static float b;
            final static boolean c;
            static final string d;
            int[002] e;
            boolean & g;
            ID[3] &h;
        }
        """
    expected = Program([ClassDecl("V", None, [
                    AttributeDecl(False, True, PrimitiveType("int"), [Attribute("a", None)]),
                    AttributeDecl(True, False, PrimitiveType("float"), [Attribute("b", None)]),
                    AttributeDecl(True, True, PrimitiveType("boolean"), [Attribute("c", None)]),
                    AttributeDecl(True, True, PrimitiveType("string"), [Attribute("d", None)]),
                    AttributeDecl(False, False, ArrayType(PrimitiveType("int"), 2), [Attribute("e", None)]),
                    AttributeDecl(False, False, ReferenceType(PrimitiveType("boolean")), [Attribute("g", None)]),
                    AttributeDecl(False, False, ReferenceType(ArrayType(ClassType("ID"), (3))), [Attribute("h", None)])
                ])])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_016():
    source = """
        class V {
            final int& a, b := 2, c;
            static int[2] a, b, c;
            ID[3] a := "s", b := 1.2, c := 2, d := true, e := false, f := nil;
        }
        """
    expected =  Program([ClassDecl("V", None, [
                    AttributeDecl(False, True, ReferenceType(PrimitiveType("int")), [Attribute("a", None), Attribute("b", IntLiteral(2)), Attribute("c", None)]),
                    AttributeDecl(True, False, ArrayType(PrimitiveType("int"), 2), [Attribute("a", None), Attribute("b", None), Attribute("c", None)]),
                    AttributeDecl(False, False, ArrayType(ClassType("ID"), (3)), [Attribute("a", StringLiteral('s')), Attribute("b", FloatLiteral(1.2)), Attribute("c", IntLiteral(2)), Attribute("d", BoolLiteral(True)), Attribute("e", BoolLiteral(False)), Attribute("f", NilLiteral())]),
                ])])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_019():
    source = """
    class V {
        int a := a.b.c + this.a.b;
        int b := a.b.c() + this.a();
        int c := a.b().c.d(1, 2)[3];
    }
    """
    expected = Program([
            ClassDecl("V", None, [
                AttributeDecl(
                    False, False, PrimitiveType("int"), [
                        Attribute(
                            "a",
                            BinaryOp(
                                PostfixExpression(
                                    Identifier("a"),
                                    [MemberAccess("b"), MemberAccess("c")]
                                ),
                                "+",
                                PostfixExpression(
                                    ThisExpression(),
                                    [MemberAccess("a"), MemberAccess("b")]
                                )
                            )
                        )
                    ]
                ),
                AttributeDecl(
                    False, False, PrimitiveType("int"), [
                        Attribute(
                            "b",
                            BinaryOp(
                                PostfixExpression(
                                    Identifier("a"),
                                    [MemberAccess("b"), MethodCall("c", [])]
                                ),
                                "+",
                                PostfixExpression(
                                    ThisExpression(),
                                    [MethodCall("a", [])]
                                )
                            )
                        )
                    ]
                ),
                AttributeDecl(
                    False, False, PrimitiveType("int"), [
                        Attribute(
                            "c",
                            PostfixExpression(
                                Identifier("a"),
                                [MethodCall("b", []), MemberAccess("c"), MethodCall("d", [IntLiteral(1), IntLiteral(2)]), ArrayAccess(IntLiteral(3))]
                            )
                        )
                    ]
                )
            ])
        ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_021():
    source = """
    class V {
        int a := -1 + +1;
        int c := -+-a[2];
    }
    """
    expected = Program([ClassDecl("V", None, [
            AttributeDecl(False, False, PrimitiveType("int"), [Attribute("a", BinaryOp(UnaryOp("-", IntLiteral(1)), "+", UnaryOp("+", IntLiteral(1))))]),
            AttributeDecl(False, False, PrimitiveType("int"), [Attribute("c", UnaryOp("-", UnaryOp("+", UnaryOp("-", PostfixExpression(Identifier("a"), [ArrayAccess(IntLiteral(2))])))))])])])
    assert str(ASTGenerator(source).generate()) == str(expected)