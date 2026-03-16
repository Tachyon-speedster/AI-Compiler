from compiler.frontend.ir import Assign, AddAssign, ForLoop, VectorAdd, VectorScale


def optimize(ir_program):

    # Handle both IRProgram and raw list
    if hasattr(ir_program, "instructions"):
        instructions = ir_program.instructions
        is_object = True
    else:
        instructions = ir_program
        is_object = False

    optimized = []
    skip_next = False

    for i, instr in enumerate(instructions):

        if skip_next:
            skip_next = False
            continue

        # Detect pattern: Assign + ForLoop summation
        if (
            i + 1 < len(instructions)
            and isinstance(instr, Assign)
            and isinstance(instructions[i + 1], ForLoop)
        ):

            assign = instr
            loop = instructions[i + 1]

            if len(loop.body) == 1:

                child = loop.body[0]

                if isinstance(child, AddAssign) and child.name == assign.name:

                    optimized.append({
                        "type": "optimized_sum",
                        "target": assign.name,
                        "limit": loop.limit
                    })

                    skip_next = True
                    continue

        optimized.append(instr)

    # Return same structure that came in
    if is_object:
        ir_program.instructions = optimized
        return ir_program
    else:
        return optimized


def apply_parallel(ir_program):

    # Handle both formats
    if hasattr(ir_program, "instructions"):
        instructions = ir_program.instructions
    else:
        instructions = ir_program

    for instr in instructions:

        if isinstance(instr, ForLoop):

            instr.parallel = True

    return ir_program

def detect_vectorization(ir_program):

    optimized = []

    for instr in ir_program:

        if instr._class.name_ == "ForLoop":

            if len(instr.body) == 1:

                child = instr.body[0]

                # arr[i] = arr[i] * constant
                if hasattr(child, "op") and child.op == "mul":

                    optimized.append(
                        VectorScale(child.name, child.value, instr.limit)
                    )
                    continue

        optimized.append(instr)

    return optimized
