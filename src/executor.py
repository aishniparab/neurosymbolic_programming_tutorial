"""
class ProgramExecutor(CLEVR_DSL):
    def __init__(self):
        super().__init__()
        pass

    def execute(self, function, params, output):
        output = self.str2func[function](output)
        return output

    def __call__(self, scene, program):
        self.scene = scene
        output = None
        for seq in program:
            args = seq.split()
            prev_out = self.execute(args[0], args[1], output)
        return output
"""