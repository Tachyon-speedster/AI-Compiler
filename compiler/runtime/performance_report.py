def generate_report(patterns, complexity, py_time, cpp_time, rust_time):

    print("\nAI Performance Report")
    print("---------------------")

    if patterns:
        for p in patterns:
            print("Detected pattern:", p["pattern"])
            print("Original complexity:", p["complexity"])
            print("Suggestion:", p["suggestion"])
            print()
    else:
        print("No known algorithm pattern detected.")
        print()

    print("Static complexity estimate:", complexity)
    print()

    fastest = min(py_time, cpp_time, rust_time)

    speedup = py_time / fastest if fastest > 0 else 0

    print("Measured Performance")
    print("--------------------")
    print("Python time:", py_time)
    print("C++ time:", cpp_time)
    print("Rust time:", rust_time)
    print()

    print("Estimated speedup vs Python: {:.2f}x".format(speedup))
