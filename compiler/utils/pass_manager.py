class PassManager:

    def __init__(self):
        self.passes = []

    def add_pass(self, optimization_pass):
        self.passes.append(optimization_pass)

    def run(self, ir_program):

        for p in self.passes:
            ir_program = p(ir_program)

        return ir_program
