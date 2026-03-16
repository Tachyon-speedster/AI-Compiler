import time
from compiler.backend.cpp_backend import generate_cpp
from compiler.runtime.runner import compile_cpp, run_cpp


def benchmark_versions(candidates):

    results = {}

    for name, ir in candidates.items():

        cpp_code = generate_cpp(ir)

        path = f"generated/{name}.cpp"

        with open(path, "w") as f:
            f.write(cpp_code)

        if not compile_cpp(path, f"generated/{name}_program"):
            results[name] = float("inf")
            continue

        start = time.time()
        run_cpp(f"./generated/{name}_program")
        end = time.time()

        results[name] = end - start

    return results
