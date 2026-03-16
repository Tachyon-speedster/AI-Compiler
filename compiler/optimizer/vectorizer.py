from copy import deepcopy


class VectorAdd:
    def __init__(self, target, left, right, length):
        self.target = target
        self.left = left
        self.right = right
        self.length = length

    def __repr__(self):
        return f"VectorAdd({self.target}, {self.left}, {self.right}, {self.length})"


class VectorScale:
    def __init__(self, target, source, scalar, length):
        self.target = target
        self.source = source
        self.scalar = scalar
        self.length = length

    def __repr__(self):
        return f"VectorScale({self.target}, {self.source}, {self.scalar}, {self.length})"


def _is_vector_add_loop(instr):
    if not isinstance(instr, dict):
        return None

    if instr.get("type") != "for":
        return None

    body = instr.get("body", [])
    if len(body) != 1:
        return None

    stmt = body[0]
    if not isinstance(stmt, dict):
        return None

    if stmt.get("type") != "assign":
        return None

    target = stmt.get("target")
    value = stmt.get("value")

    if not isinstance(target, dict) or not isinstance(value, dict):
        return None

    if target.get("type") != "index":
        return None

    if value.get("type") != "binop" or value.get("op") != "+":
        return None

    left = value.get("left")
    right = value.get("right")

    if not isinstance(left, dict) or not isinstance(right, dict):
        return None

    if left.get("type") != "index" or right.get("type") != "index":
        return None

    return {
        "target": target.get("value"),
        "left": left.get("value"),
        "right": right.get("value"),
        "length": instr.get("iter"),
    }


def _is_vector_scale_loop(instr):
    if not isinstance(instr, dict):
        return None

    if instr.get("type") != "for":
        return None

    body = instr.get("body", [])
    if len(body) != 1:
        return None

    stmt = body[0]
    if not isinstance(stmt, dict):
        return None

    if stmt.get("type") != "assign":
        return None

    target = stmt.get("target")
    value = stmt.get("value")

    if not isinstance(target, dict) or not isinstance(value, dict):
        return None

    if target.get("type") != "index":
        return None

    if value.get("type") != "binop" or value.get("op") != "*":
        return None

    left = value.get("left")
    right = value.get("right")

    if not isinstance(left, dict) or not isinstance(right, dict):
        return None

    if left.get("type") == "index" and right.get("type") == "const":
        return {
            "target": target.get("value"),
            "source": left.get("value"),
            "scalar": right.get("value"),
            "length": instr.get("iter"),
        }

    if right.get("type") == "index" and left.get("type") == "const":
        return {
            "target": target.get("value"),
            "source": right.get("value"),
            "scalar": left.get("value"),
            "length": instr.get("iter"),
        }

    return None


def vectorize(ir):
    """
    Replace simple elementwise loops with vector IR nodes.
    """
    if not isinstance(ir, list):
        return ir

    new_ir = []
    for instr in deepcopy(ir):
        add_match = _is_vector_add_loop(instr)
        if add_match:
            new_ir.append(
                VectorAdd(
                    add_match["target"],
                    add_match["left"],
                    add_match["right"],
                    add_match["length"],
                )
            )
            continue

        scale_match = _is_vector_scale_loop(instr)
        if scale_match:
            new_ir.append(
                VectorScale(
                    scale_match["target"],
                    scale_match["source"],
                    scale_match["scalar"],
                    scale_match["length"],
                )
            )
            continue

        new_ir.append(instr)

    return new_ir


def vectorize_loops(ir):
    return vectorize(ir)
