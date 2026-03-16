def parallelize_loops(ir_program):

    new_ir = []

    for instr in ir_program:

        if instr.__class__.__name__ == "ForLoop":

            if len(instr.body) == 1:

                new_ir.append({
                    "type": "parallel_loop",
                    "var": instr.var,
                    "limit": instr.limit,
                    "body": instr.body
                })

                continue

        new_ir.append(instr)

    return new_ir
