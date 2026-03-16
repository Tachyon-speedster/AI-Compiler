from compiler.frontend.ir import Assign


def fold_constants(ir_program):

    new_ir = []

    for instr in ir_program:

        if isinstance(instr, Assign):

            try:

                # try computing value at compile time
                value = eval(str(instr.value))

                instr.value = value

            except:

                pass

        new_ir.append(instr)

    return new_ir
