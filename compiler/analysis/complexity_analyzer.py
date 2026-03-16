from compiler.frontend.ir import ForLoop


def analyze_complexity(ir_program):

    loop_depth = 0
    max_depth = 0

    def scan(nodes, depth=0):
        nonlocal max_depth

        for node in nodes:

            if isinstance(node, ForLoop):
                depth += 1
                max_depth = max(max_depth, depth)
                scan(node.body, depth)
                depth -= 1

    scan(ir_program)

    if max_depth == 0:
        return "O(1)"
    elif max_depth == 1:
        return "O(n)"
    elif max_depth == 2:
        return "O(n^2)"
    elif max_depth == 3:
        return "O(n^3)"
    else:
        return f"O(n^{max_depth})"

