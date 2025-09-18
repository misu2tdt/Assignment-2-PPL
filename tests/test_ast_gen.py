from utils import ASTGenerator
from src.utils.nodes import *


def test_001():
    """Test basic class declaration AST generation"""
    source = """class TestClass {
        int x;
    }"""
    expected = Program([ClassDecl("TestClass", None, [AttributeDecl(False, False, PrimitiveType("int"), [Attribute("x", None)])])])
    # Just check that it doesn't return an error
    assert str(ASTGenerator(source).generate()) == str(expected)


def test_002():
    """Test class with method declaration AST generation"""
    source = """class TestClass {
        void main() {
            return;
        }
    }"""
    expected = Program([ClassDecl("TestClass", None, [MethodDecl(False, PrimitiveType("void"), "main", [], BlockStatement([], [ReturnStatement(NilLiteral())]))])])
    assert str(ASTGenerator(source).generate()) == str(expected)


def test_003():
    """Test class with constructor AST generation"""
    source = """class TestClass {
        int x;
        TestClass(int x) {
            this.x := x;
        }
    }"""
    expected = Program([ClassDecl("TestClass", None, [AttributeDecl(False, False, PrimitiveType("int"), [Attribute("x", None)]), ConstructorDecl("TestClass", [Parameter(PrimitiveType("int"), "x")], BlockStatement([], [AssignmentStatement(PostfixLHS(PostfixExpression(ThisExpression(), MemberAccess("x"))), Identifier("x"))]))])])
    assert str(ASTGenerator(source).generate()) == str(expected)


def test_004():
    """Test class with inheritance AST generation"""
    source = """class Child extends Parent {
        int y;
    }"""
    expected = Program([ClassDecl("Child", "Parent", [AttributeDecl(False, False, PrimitiveType("int"), [Attribute("y", None)])])])
    assert str(ASTGenerator(source).generate()) == str(expected)


def test_005():
    """Test static and final attributes AST generation"""
    source = """class TestClass {
        static final int MAX_SIZE := 100;
        final float PI := 3.14;
    }"""
    expected = Program([ClassDecl("TestClass", None, [AttributeDecl(True, True, PrimitiveType("int"), [Attribute("MAX_SIZE", IntLiteral(100))]), AttributeDecl(False, True, PrimitiveType("float"), [Attribute("PI", FloatLiteral(3.14))])])])
    assert str(ASTGenerator(source).generate()) == str(expected)


def test_006():
    """Test if-else statement AST generation"""
    source = """class TestClass {
        void main() {
            if (x > 0) then {
                return x;
            } else {
                return 0;
            }
        }
    }"""
    expected = Program([ClassDecl("TestClass", None, [MethodDecl(False, PrimitiveType("void"), "main", [], BlockStatement([], [IfStatement(ParenthesizedExpression((BinaryOp(Identifier("x"), ">", IntLiteral(0)))), BlockStatement([], [ReturnStatement(Identifier("x"))]), BlockStatement([], [ReturnStatement(IntLiteral(0))]))]))])])
    assert str(ASTGenerator(source).generate()) == str(expected)


def test_007():
    """Test for loop AST generation"""
    source = """class TestClass {
        void main() {
            for i := 1 to 10 do {
                io.writeIntLn(i);
            }
        }
    }"""
    expected = Program([ClassDecl("TestClass", None, [MethodDecl(False, PrimitiveType("void"), "main", [], BlockStatement([], [ForStatement("i", IntLiteral(1), "to", IntLiteral(10), BlockStatement([], [MethodInvocationStatement(MethodInvocation(PostfixExpression(Identifier("io"), MethodCall("writeIntLn", [Identifier("i")]))))]))]))])])
    assert str(ASTGenerator(source).generate()) == str(expected)


def test_008():
    """Test array operations AST generation"""
    source = """class TestClass {
        void main() {
            int[5] arr;
            arr[0] := 42;
        }
    }"""
    expected = Program([ClassDecl("TestClass", None, [MethodDecl(False, PrimitiveType("void"), "main", [], BlockStatement([VariableDecl(False, ArrayType(PrimitiveType("int"), IntLiteral(5)), [Variable("arr", None)])] , [AssignmentStatement(PostfixLHS(PostfixExpression(Identifier("arr"), ArrayAccess(IntLiteral(0)))), IntLiteral(42))]))])])
    assert str(ASTGenerator(source).generate()) == str(expected)


def test_009():
    """Test object creation and method call AST generation"""
    source = """class TestClass {
        void main() {
            Rectangle r := new Rectangle(5.0, 3.0);
            float area := r.getArea();
        }
    }"""
    expected = Program([ClassDecl("TestClass", None, [MethodDecl(False, PrimitiveType("void"), "main", [], BlockStatement([VariableDecl(False, ClassType("Rectangle"), [Variable("r", ObjectCreation("Rectangle", [FloatLiteral(5.0), FloatLiteral(3.0)]))]), VariableDecl(False, PrimitiveType("float"), [Variable("area", PostfixExpression(Identifier("r"), MethodCall("getArea", [])))])] , []))])])
    assert str(ASTGenerator(source).generate()) == str(expected)


def test_010():
    """Test reference type AST generation"""
    source = """class TestClass {
        void swap(int & a; int & b) {
            int temp := a;
            a := b;
            b := temp;
        }
    }"""
    expected = Program([ClassDecl("TestClass", None, [MethodDecl(False, PrimitiveType("void"), "swap", [Parameter(ReferenceType(PrimitiveType("int")), "a"), Parameter(ReferenceType(PrimitiveType("int")), "b")], BlockStatement([VariableDecl(False, PrimitiveType("int"), [Variable("temp", Identifier("a"))])] , [AssignmentStatement(IdLHS("a"), Identifier("b")), AssignmentStatement(IdLHS("b"), Identifier("temp"))]))])])
    assert str(ASTGenerator(source).generate()) == str(expected)


def test_011():
    """Test destructor AST generation"""
    source = """class TestClass {
        ~TestClass() {
            io.writeStrLn("Object destroyed");
        }
    }"""
    expected = Program([ClassDecl("TestClass", None, [DestructorDecl("TestClass", BlockStatement([], [MethodInvocationStatement(MethodInvocation(PostfixExpression(Identifier("io"), MethodCall("writeStrLn", [StringLiteral('Object destroyed')]))))]))])])
    assert str(ASTGenerator(source).generate()) == str(expected)


def test_012():
    """Test static method invocation AST generation"""
    source = """class TestClass {
        void main() {
            int count := Shape.getCount();
        }
    }"""
    expected = Program([ClassDecl("TestClass", None, [MethodDecl(False, PrimitiveType("void"), "main", [], BlockStatement([VariableDecl(False, PrimitiveType("int"), [Variable("count", PostfixExpression(Identifier("Shape"), MethodCall("getCount", [])))])] , []))])])
    assert str(ASTGenerator(source).generate()) == str(expected)