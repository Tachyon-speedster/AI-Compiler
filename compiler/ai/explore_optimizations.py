from compiler.ai.candidate_generator import generate_candidates
from compiler.runtime.auto_benchmark import benchmark_versions


def explore(ir):

    candidates = generate_candidates(ir)

    results = benchmark_versions(candidates)

    print("\nAuto Optimization Results")
    print("------------------------")

    for k, v in results.items():
        print(k, ":", v)

    best = min(results, key=results.get)

    print("Best optimization:", best)

    return best
