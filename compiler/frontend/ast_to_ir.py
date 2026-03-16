
import ast
from compiler.frontend.ir import Assign, AddAssign, ForLoop, Print, VectorAdd


class IRBuilder(ast.NodeVisitor):

    def __init__(self):
        self.ir = []

    # -------------------------
    # Assign
    # -------------------------

    def visit_Assign(self, node):

        target = node.targets[0]

        # detect vector add pattern
        if isinstance(node.value, ast.BinOp):

            if isinstance(node.value.op, ast.Add):

                if isinstance(node.value.left, ast.Subscript) and isinstance(node.value.right, ast.Subscript):

                    a = node.value.left.value.id
                    b = node.value.right.value.id
                    dest = target.value.id

                    self.ir.append(
                        VectorAdd(a, b, dest, "N")
                    )

                    return

        # simple assignment
        if isinstance(target, ast.Name):

            value = self._expr(node.value)

            self.ir.append(
                Assign(target.id, value)
            )

    # -------------------------
    # Augmented assignment
    # -------------------------

    def visit_AugAssign(self, node):

        if isinstance(node.op, ast.Add):

            if isinstance(node.target, ast.Name):

                value = self._expr(node.value)

                self.ir.append(
                    AddAssign(node.target.id, value)
                )

    # -------------------------
    # For loops
    # -------------------------

    def visit_For(self, node):

        if isinstance(node.iter, ast.Call):

            if node.iter.func.id == "range":

                limit = self._expr(node.iter.args[0])

                loop = ForLoop(node.target.id, limit, [])

                # process body
                for stmt in node.body:

                    if isinstance(stmt, ast.AugAssign):

                        if isinstance(stmt.op, ast.Add):

                            val = self._expr(stmt.value)

                            loop.body.append(
                                AddAssign(stmt.target.id, val)
                            )

                self.ir.append(loop)

    # -------------------------
    # Print
    # -------------------------

    def visit_Expr(self, node):

        if isinstance(node.value, ast.Call):

            if node.value.func.id == "print":

                val = self._expr(node.value.args[0])

                self.ir.append(
                    Print(val)
                )

    # -------------------------
    # Expression parser
    # -------------------------

    def _expr(self, node):

        if isinstance(node, ast.Constant):
            return node.value

        if isinstance(node, ast.Name):
            return node.id

        if isinstance(node, ast.BinOp):

            left = self._expr(node.left)
            right = self._expr(node.right)

            if isinstance(node.op, ast.Add):
                return f"{left}+{right}"

            if isinstance(node.op, ast.Sub):
                return f"{left}-{right}"

            if isinstance(node.op, ast.Mult):
                return f"{left}*{right}"

        return "0"


def build_ir(tree):

    builder = IRBuilder()

    builder.visit(tree)

    return builder.ir
