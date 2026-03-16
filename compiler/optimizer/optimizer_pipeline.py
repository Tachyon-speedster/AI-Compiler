from copy import deepcopy

from compiler.optimizer.constant_folding import fold_constants
from compiler.optimizer.loop_optimizer import unroll_loops
from compiler.optimizer.vectorizer import vectorize
from compiler.optimizer.loop_tiling import tile_loops


def optimize_ir(ir):
    current = deepcopy(ir)

    print("Running Optimization Pipeline")
    print("-----------------------------")

    print("Pass 1: Constant Folding")
    current = fold_constants(current)

    print("Pass 2: Loop Unrolling")
    current = unroll_loops(current)

    print("Pass 3: Vectorization")
    current = vectorize(current)

    print("Pass 4: Loop Tiling")
    current = tile_loops(current)

    print("Optimization Pipeline Complete")
    print()

    return current
