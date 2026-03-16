def analyze_space(ir_program):

    variables = set()
    arrays = 0

    for instr in ir_program:

        # Track variable assignments
        if instr.__class__.__name__ == "Assign":
            variables.add(instr.name)

        # Track loop variables
        if instr.__class__.__name__ == "ForLoop":
            variables.add(instr.var)

    # Simple heuristic
    if len(variables) <= 3:
        return "O(1)"
    else:
        return f"O({len(variables)})"
