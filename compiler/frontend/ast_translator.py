import ast

class CPPGenerator(ast.NodeVisitor):

    def __init__(self):
        self.code = []
        self.indent = 1

    def emit(self, line):
        self.code.append("    " * self.indent + line)

    # variable assignment
    def visit_Assign(self, node):

        var = node.targets[0].id
        value = ast.unparse(node.value)

        self.emit(f"long long {var} = {value};")

    # += operations
    def visit_AugAssign(self, node):

        var = node.target.id
        value = ast.unparse(node.value)

        self.emit(f"{var} += {value};")

    # for loops
    def visit_For(self, node):

        var = node.target.id
        limit = ast.unparse(node.iter.args[0])

        self.emit(f"for(long long {var}=0; {var}<{limit}; {var}++)"+" {")

        self.indent += 1

        for stmt in node.body:
            self.visit(stmt)

        self.indent -= 1
        self.emit("}")

    # print
    def visit_Expr(self, node):

        if isinstance(node.value, ast.Call):

            if node.value.func.id == "print":

                arg = ast.unparse(node.value.args[0])

                self.emit(f"cout << {arg} << endl;")

def python_to_cpp(code):

    tree = ast.parse(code)

    generator = CPPGenerator()

    header = [
        "#include <iostream>",
        "using namespace std;",
        "",
        "int main(){"
    ]

    generator.code = header

    for stmt in tree.body:
        generator.visit(stmt)

    generator.code.append("return 0;")
    generator.code.append("}")

    return "\n".join(generator.code)
