from utils import Parser


def test_001():
    """Test basic class with main method"""
    source = """class Program { static void main() {} }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_002():
    """Test method with parameters"""
    source = """class Math { int add(int a; int b) { return a + b; } }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_003():
    """Test class with attribute declaration"""
    source = """class Test { int x; static void main() { x := 42; } }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_004():
    """Test class with string attribute"""
    source = """class Test { string name; static void main() { name := "Alice"; } }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_005():
    """Test final attribute declaration"""
    source = """class Constants { final float PI = 3.14159; static void main() {} }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_006():
    """Test if-else statement"""
    source = """class Test { 
        static void main() { 
            if (x > 0) then { 
                io.writeStrLn("positive"); 
            } else { 
                io.writeStrLn("negative"); 
            }
        }
    }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_007():
    """Test for loop with to keyword"""
    source = """class Test { 
        static void main() { 
            int i;
            for i := 1 to 10 do { 
                i := i + 1; 
            }
        }
    }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_008():
    """Test for loop with downto keyword"""
    source = """class Test { 
        static void main() { 
            int i;
            for i := 10 downto 1 do { 
                io.writeInt(i); 
            }
        }
    }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_009():
    """Test array declaration and access"""
    source = """class Test { 
        static void main() { 
            int[3] arr = {1, 2, 3};
            int first;
            first := arr[0];
            arr[1] := 42;
        }
    }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_010():
    """Test string concatenation and object creation"""
    source = """class Test { 
        static void main() { 
            string result;
            result := "Hello" ^ " " ^ "World";
            Test obj;
            obj := new Test();
        }
    }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_011():
    """Test parser error: missing closing brace in class declaration"""
    source = """class Test { int x = 1; """  # Thiếu dấu }
    expected = "Error on line 1 col 24: <EOF>"
    assert Parser(source).parse() == expected

def test_012():
    """Example 1"""
    source = """
class Example1 {
    int factorial(int n){
        if n == 0 then return 1; else return n * this.factorial(n - 1);
    }

    void main(){
        int x;
        x := io.readInt();
        io.writeIntLn(this.factorial(x));
    }
}
""" 
    expected = "success"
    assert Parser(source).parse() == expected

def test_013():
    """Example 2"""
    source = """
class Shape {
    float length, width;
    float getArea() {}
    Shape(float length, width){
        this.length := length;
        this.width := width;
    }
}

class Rectangle extends Shape {
    float getArea(){
        return this.length * this.width;
    }
}

class Triangle extends Shape {
    float getArea(){
        return this.length * this.width / 2;
    }
}

class Example2 {
    void main(){
        Shape s;
        s := new Rectangle(3,4);
        io.writeFloatLn(s.getArea());
        s := new Triangle(3,4);
        io.writeFloatLn(s.getArea());
    }
}
""" 
    expected = "success"
    assert Parser(source).parse() == expected

def test_014():
    """Example 3"""
    source = """
class Rectangle {
    float length, width;
    static int count;
    
    ## Default constructor
    Rectangle() {
        this.length := 1.0;
        this.width := 1.0;
        Rectangle.count := Rectangle.count + 1;
    }
    
    ## Copy constructor
    Rectangle(Rectangle other) {
        this.length := other.length;
        this.width := other.width;
        Rectangle.count := Rectangle.count + 1;
    }
    
    ## User-defined constructor
    Rectangle(float length, width) {
        this.length := length;
        this.width := width;
        Rectangle.count := Rectangle.count + 1;
    }
    
    ## Destructor
    ~Rectangle() {
        Rectangle.count := Rectangle.count - 1;
        io.writeStrLn("Rectangle destroyed");
    }
    
    float getArea() {
        return this.length * this.width;
    }
    
    static int getCount() {
        return Rectangle.count;
    }
}

class Example3 {
    void main() {
        ## Using different constructors
        Rectangle r1 = new Rectangle();           ## Default constructor
        Rectangle r2 = new Rectangle(5.0, 3.0);  ## User-defined constructor
        Rectangle r3 = new Rectangle(r2);        ## Copy constructor
        
        io.writeFloatLn(r1.getArea());  ## 1.0
        io.writeFloatLn(r2.getArea());  ## 15.0
        io.writeFloatLn(r3.getArea());  ## 15.0
        io.writeIntLn(Rectangle.getCount());  ## 3
        
        ## Destructors will be called automatically when objects go out of scope
    }
}
""" 
    expected = "success"
    assert Parser(source).parse() == expected

def test_015():
    """Example 4"""
    source = """
class MathUtils {
    static void swap(int & a; int & b) {
        int temp = a;
        a := b;
        b := temp;
    }
    
    static void modifyArray(int[5] & arr; int index; int value) {
        arr[index] := value;
    }
    
    static int & findMax(int[5] & arr) {
        int & max = arr[0];
        for i := 1 to 4 do {
            if (arr[i] > max) then {
                max := arr[i];
            }
        }
        return max;
    }
}

class StringBuilder {
    string & content;
    
    StringBuilder(string & content) {
        this.content := content;
    }
    
    StringBuilder & append(string & text) {
        this.content := this.content ^ text;
        return this;
    }
    
    StringBuilder & appendLine(string & text) {
        this.content := this.content ^ text ^ "\\n";
        return this;
    }
    
    string & toString() {
        return this.content;
    }
}

class Example4 {
    void main() {
        ## Reference variables
        int x = 10, y = 20;
        int & xRef = x;
        int & yRef = y;
        
        io.writeIntLn(xRef);  ## 10
        io.writeIntLn(yRef);  ## 20
        
        ## Pass by reference
        MathUtils.swap(x, y);
        io.writeIntLn(x);  ## 20
        io.writeIntLn(y);  ## 10
        
        ## Array references
        int[5] numbers = {1, 2, 3, 4, 5};
        MathUtils.modifyArray(numbers, 2, 99);
        io.writeIntLn(numbers[2]);  ## 99
        
        ## Reference return
        int & maxRef = MathUtils.findMax(numbers);
        maxRef := 100;
        io.writeIntLn(numbers[2]);  ## 100
        
        ## Method chaining with references
        string text = "Hello";
        StringBuilder & builder = new StringBuilder(text);
        builder.append(" ").append("World").appendLine("!");
        io.writeStrLn(builder.toString());  ## "Hello World!\\n"
    }
}
""" 
    expected = "success"
    assert Parser(source).parse() == expected
