from compiler.frontend.ir import Assign, AddAssign, ForLoop, Print, VectorAdd, TiledLoop


def generate_rust(ir_program):

    lines = []

    lines.append("use std::arch::x86_64::*;")
    lines.append("")
    lines.append("fn main(){")

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
                    f"let mut {target}: i64 = ({limit} * ({limit}-1))/2;"
                )

                declared.add(target)

        # -------------------------
        # Assign
        # -------------------------

        elif isinstance(instr, Assign):

            if instr.name not in declared:

                lines.append(
                    f"let mut {instr.name}: i64 = {instr.value};"
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
                f'println!("{{}}", {instr.value});'
            )

        # -------------------------
        # SIMD Vector Add
        # -------------------------

        elif isinstance(instr, VectorAdd):

            lines.append("unsafe {")

            lines.append("let mut i = 0;")

            lines.append(f"while i < {instr.size} {{")

            lines.append(
                f"let va = _mm256_loadu_pd({instr.a}.as_ptr().add(i));"
            )

            lines.append(
                f"let vb = _mm256_loadu_pd({instr.b}.as_ptr().add(i));"
            )

            lines.append(
                "let vc = _mm256_add_pd(va,vb);"
            )

            lines.append(
                f"_mm256_storeu_pd({instr.dest}.as_mut_ptr().add(i),vc);"
            )

            lines.append("i += 4;")

            lines.append("}")

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

                lines.append(f"let mut {target}: i64 = 0;")

                declared.add(target)

            lines.append(
                f"for {instr.var} in 0..{instr.limit} {{"
            )

            for child in instr.body:

                if isinstance(child, AddAssign):

                    lines.append(
                        f"{child.name} += {instr.var};"
                    )

            lines.append("}")

        elif isinstance(instr, TiledLoop):

            T = instr.tile_size
            N = instr.limit

            lines.append(f"for ii in (0..{N}).step_by({T}) {{")
            lines.append(f"for jj in (0..{N}).step_by({T}) {{")

            lines.append(f"for {instr.outer_var} in ii..std::cmp::min(ii+{T},{N}) {{")
            lines.append(f"for {instr.inner_var} in jj..std::cmp::min(jj+{T},{N}) {{")

            lines.append("// tiled operation")

            lines.append("}")
            lines.append("}")
            lines.append("}")
            lines.append("}")

    lines.append("}")

    return "\n".join(lines)


# -----------------------------
# Create Cargo Project
# -----------------------------

import os


def create_rust_project(code):

    os.makedirs("generated/src", exist_ok=True)

    with open("generated/src/main.rs", "w") as f:
        f.write(code)

    cargo = """
[package]
name = "generated"
version = "0.1.0"
edition = "2021"

[dependencies]
"""

    with open("generated/Cargo.toml", "w") as f:
        f.write(cargo)
