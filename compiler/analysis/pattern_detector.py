def detect_patterns(ir_program):

    patterns = []

    for instr in ir_program:

        # -------------------------
        # Arithmetic Summation Loop
        # -------------------------
        if instr.__class__.__name__ == "ForLoop":

            if len(instr.body) == 1:

                child = instr.body[0]

                if child.__class__.__name__ == "AddAssign":

                    patterns.append({
                        "pattern": "Arithmetic Summation Loop",
                        "complexity": "O(n)",
                        "suggestion": "Use formula n(n-1)/2"
                    })

        # -------------------------
        # Nested Loops
        # -------------------------
        if instr.__class__.__name__ == "ForLoop":

            for child in instr.body:

                if child.__class__.__name__ == "ForLoop":

                    patterns.append({
                        "pattern": "Nested Loop",
                        "complexity": "O(n²)",
                        "suggestion": "Consider optimizing algorithm or reducing nested loops"
                    })

        # -------------------------
        # Linear Loop
        # -------------------------
        if instr.__class__.__name__ == "ForLoop":

            patterns.append({
                "pattern": "Linear Iteration",
                "complexity": "O(n)",
                "suggestion": "Check if loop can be vectorized or parallelized"
            })

    return patterns
