from compiler.optimizer.optimizer import optimize, apply_parallel
from compiler.optimizer.vectorizer import vectorize
from compiler.optimizer.loop_tiling import apply_loop_tiling


def generate_candidates(ir):

    candidates = {}

    candidates["none"] = ir

    try:
        candidates["formula"] = optimize(ir)
    except:
        pass

    try:
        candidates["parallel"] = apply_parallel(ir)
    except:
        pass

    try:
        candidates["vector"] = vectorize(ir)
    except:
        pass

    try:
        candidates["tiling"] = apply_loop_tiling(ir)
    except:
        pass

    return candidates
