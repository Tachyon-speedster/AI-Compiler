from compiler.frontend.ir import (
    Assign,
    AddAssign,
    ForLoop,
    Print,
    VectorAdd,
    VectorScale,
    TiledLoop
)


def extract_features(ir_program):

    features = {
        "num_instructions": 0,
        "num_loops": 0,
        "nested_loops": 0,
        "max_loop_depth": 0,
        "assignments": 0,
        "add_assign": 0,
        "prints": 0,
        "vector_ops": 0,
        "vector_add": 0,
        "vector_scale": 0,
        "operations": 0,
        "memory_ops": 0,
        "tiled_loops": 0
    }

    # -----------------------------
    # Track loop depth
    # -----------------------------

    def analyze_block(block, depth=0):

        local_loop_found = False

        for instr in block:

            features["num_instructions"] += 1

            # -------------------------
            # Assign
            # -------------------------

            if isinstance(instr, Assign):

                features["assignments"] += 1
                features["operations"] += 1

            # -------------------------
            # AddAssign
            # -------------------------

            elif isinstance(instr, AddAssign):

                features["add_assign"] += 1
                features["operations"] += 1

            # -------------------------
            # Print
            # -------------------------

            elif isinstance(instr, Print):

                features["prints"] += 1

            # -------------------------
            # Vector Operations
            # -------------------------

            elif isinstance(instr, VectorAdd):

                features["vector_ops"] += 1
                features["vector_add"] += 1
                features["operations"] += 1
                features["memory_ops"] += 2

            elif isinstance(instr, VectorScale):

                features["vector_ops"] += 1
                features["vector_scale"] += 1
                features["operations"] += 1
                features["memory_ops"] += 1

            # -------------------------
            # Loops
            # -------------------------

            elif isinstance(instr, ForLoop):

                features["num_loops"] += 1
                local_loop_found = True

                current_depth = depth + 1

                if current_depth > features["max_loop_depth"]:
                    features["max_loop_depth"] = current_depth

                # recursive body analysis
                analyze_block(instr.body, current_depth)

            elif isinstance(instr, TiledLoop):
                features["tiled_loops"] += 1

        # detect nested loops
        if depth > 0 and local_loop_found:
            features["nested_loops"] += 1

    # run analysis
    analyze_block(ir_program)

    return features
