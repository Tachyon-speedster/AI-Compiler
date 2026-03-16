from compiler.frontend.ir import Assign, AddAssign, ForLoop, Print


def generate_java(ir_program):

    lines = []

    lines.append("public class GeneratedProgram {")
    lines.append("public static void main(String[] args) {")
    lines.append("")

    declared = set()

    for instr in ir_program:

        # -------------------------
        # Optimized Summation (O1 formula)
        # -------------------------
        if isinstance(instr, dict) and instr["type"] == "optimized_sum":

            target = instr["target"]
            limit = instr["limit"]

            if target not in declared:
                lines.append(f"long {target} = ({limit}L * ({limit}L - 1)) / 2;")
                declared.add(target)
            else:
                lines.append(f"{target} = ({limit}L * ({limit}L - 1)) / 2;")

        # -------------------------
        # Assign
        # -------------------------
        elif isinstance(instr, Assign):

            if instr.name not in declared:

                lines.append(f"long {instr.name} = {instr.value};")
                declared.add(instr.name)

            else:

                lines.append(f"{instr.name} = {instr.value};")

        # -------------------------
        # Print
        # -------------------------
        elif isinstance(instr, Print):

            lines.append(f"System.out.println({instr.value});")

        # -------------------------
        # For Loop
        # -------------------------
        elif isinstance(instr, ForLoop):

            # ---------- PARALLEL LOOP ----------
            if hasattr(instr, "parallel") and instr.parallel:

                target = None

                for child in instr.body:
                    if isinstance(child, AddAssign):
                        target = child.name

                if target:

                    if target not in declared:

                        lines.append(
                            f"long {target} = java.util.stream.LongStream.range(0,{instr.limit}).parallel().sum();"
                        )

                        declared.add(target)

                    else:

                        lines.append(
                            f"{target} = java.util.stream.LongStream.range(0,{instr.limit}).parallel().sum();"
                        )

                continue

            # ---------- NORMAL LOOP ----------
            lines.append(
                f"for(long {instr.var}=0; {instr.var}<{instr.limit}; {instr.var}++){{"
            )

            for child in instr.body:

                if isinstance(child, AddAssign):

                    lines.append(f"{child.name} += {instr.var};")

            lines.append("}")

    lines.append("")
    lines.append("}")
    lines.append("}")

    return "\n".join(lines)
