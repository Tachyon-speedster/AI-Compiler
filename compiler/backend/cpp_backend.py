from compiler.frontend.ir import Assign, AddAssign, ForLoop, Print, VectorAdd, TiledLoop


def generate_cpp(ir_program):

    lines = []

    lines.append("#include <iostream>")
    lines.append("#include <immintrin.h>")
    lines.append("#include <algorithm>")
    lines.append("using namespace std;")
    lines.append("")
    lines.append("int main(){")

    declared = set()

    for instr in ir_program:

        # -------------------------
        # Optimized sum
        # -------------------------

        if isinstance(instr, dict) and instr.get("type") == "optimized_sum":

            target = instr["target"]
            limit = instr["limit"]

            if target not in declared:

                lines.append(
                    f"long {target} = ({limit}LL * ({limit}-1))/2;"
                )

                declared.add(target)

        # -------------------------
        # Assign
        # -------------------------

        elif isinstance(instr, Assign):

            if instr.name not in declared:

                lines.append(
                    f"long {instr.name} = {instr.value};"
                )

                declared.add(instr.name)

            else:

                lines.append(
                    f"{instr.name} = {instr.value};"
                )

        # -------------------------
        # Print
        # -------------------------

        elif isinstance(instr, Print):

            lines.append(
                f'cout << {instr.value} << endl;'
            )

        # -------------------------
        # SIMD Vector Add
        # -------------------------

        elif isinstance(instr, VectorAdd):

            lines.append(f"for(int i=0;i<{instr.size};i+=4){{")

            lines.append(
                f"__m256d va = _mm256_loadu_pd({instr.a}+i);"
            )

            lines.append(
                f"__m256d vb = _mm256_loadu_pd({instr.b}+i);"
            )

            lines.append(
                "__m256d vc = _mm256_add_pd(va,vb);"
            )

            lines.append(
                f"_mm256_storeu_pd({instr.dest}+i,vc);"
            )

            lines.append("}")

        # -------------------------
        # For Loop
        # -------------------------

        elif isinstance(instr, ForLoop):

            target = None

            for child in instr.body:
                if isinstance(child, AddAssign):
                    target = child.name

            if target and target not in declared:

                lines.append(f"long {target}=0;")

                declared.add(target)

            lines.append(
                f"for(long {instr.var}=0; {instr.var}<{instr.limit}; {instr.var}++){{"
            )

            for child in instr.body:

                if isinstance(child, AddAssign):

                    lines.append(
                        f"{child.name}+={instr.var};"
                    )

            lines.append("}")

        elif isinstance(instr, TiledLoop):

            T = instr.tile_size
            N = instr.limit

            lines.append(f"for(int ii=0; ii<{N}; ii+={T}){{")
            lines.append(f"for(int jj=0; jj<{N}; jj+={T}){{")

            lines.append(f"for(int {instr.outer_var}=ii; {instr.outer_var}<std::min(ii+{T},{N}); {instr.outer_var}++){{")
            lines.append(f"for(int {instr.inner_var}=jj; {instr.inner_var}<std::min(jj+{T},{N}); {instr.inner_var}++){{")

            for op in instr.body:
                lines.append("// tiled operation")

            lines.append("}")
            lines.append("}")
            lines.append("}")
            lines.append("}")

    lines.append("}")
    return "\n".join(lines)
