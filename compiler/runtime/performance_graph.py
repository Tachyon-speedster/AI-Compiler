import matplotlib.pyplot as plt



def plot_performance(py_time, cpp_time, rust_time, java_time):

    languages = ["Python", "C++", "Rust", "Java"]
    times = [py_time, cpp_time, rust_time, java_time]

    plt.figure()

    plt.bar(languages, times)

    plt.title("Language Performance Comparison")
    plt.ylabel("Execution Time (seconds)")
    plt.xlabel("Language")

    plt.show()

