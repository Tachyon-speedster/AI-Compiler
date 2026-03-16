def detect_parallel_loops(ir_program):

    parallel_loops = []

    for instr in ir_program:

        if instr.__class__.__name__ == "ForLoop":

            safe = True

            # check loop body for unsafe operations
            for child in instr.body:

                if child.__class__.__name__ not in ["AddAssign"]:
                    safe = False

            if safe:
                parallel_loops.append(instr)

    return parallel_loops
