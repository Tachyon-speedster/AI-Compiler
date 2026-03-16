from copy import deepcopy


def unroll_loops(ir, factor=4):
    if not isinstance(ir, list):
        return ir

    result = []

    for instr in deepcopy(ir):
        if not isinstance(instr, dict):
            result.append(instr)
            continue

        if instr.get("type") != "for":
            result.append(instr)
            continue

        loop_count = instr.get("iter")
        body = instr.get("body", [])

        if not isinstance(loop_count, int) or loop_count <= 0:
            result.append(instr)
            continue

        if loop_count > 16:
            result.append(instr)
            continue

        for _ in range(loop_count):
            for stmt in body:
                result.append(deepcopy(stmt))

    return result

def optimize_loops(ir):
    return unroll_loops(ir)
