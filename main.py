import os
import ast

# Optimizer pipeline
from compiler.optimizer.optimizer_pipeline import optimize_ir
from compiler.optimizer.optimization_suggester import suggest_optimizations

# AI system
from compiler.ai.feature_extractor import extract_features
from compiler.ai.explore_optimizations import explore
from compiler.ai.learning_engine import init_dataset, store_training_example
from compiler.ai.auto_train import retrain
from compiler.ai.ai_optimizer import ai_select
from compiler.ai.auto_dataset_builder import build_dataset

# Static analysis
from compiler.analysis.space_analyzer import analyze_space
from compiler.analysis.pattern_detector import detect_patterns
from compiler.analysis.complexity_analyzer import analyze_complexity

# Backends
from compiler.backend.cpp_backend import generate_cpp
from compiler.backend.rust_backend import generate_rust, create_rust_project
from compiler.backend.java_backend import generate_java

# Runtime / benchmarking
from compiler.runtime.runner import (
    compile_java,
    run_java,
    run_rust,
    compile_cpp,
    compile_rust,
    run_cpp
)

from compiler.runtime.benchmark import run_python
from compiler.runtime.performance_graph import plot_performance
from compiler.runtime.performance_report import generate_report

# Frontend
from compiler.frontend.ast_to_ir import build_ir

# Utilities
from compiler.utils.project_scanner import scan_project


print("""
========================================
   AI Self-Learning Python Compiler
========================================
Pipeline:
Python → IR → AI Optimization → C++ / Rust / Java
Automatic Performance Benchmarking
========================================
""")

path = input("Enter Python file or project folder: ")

if os.path.isfile(path):
    files = [path]

elif os.path.isdir(path):
    files = scan_project(path)

else:
    print("Invalid path.")
    exit()


os.makedirs("generated", exist_ok=True)

init_dataset()

train_choice = input("Generate synthetic training data? (y/n): ").lower()

if train_choice == "y":

    print("\nGenerating training programs...\n")

    build_dataset(50)

    print("\nRetraining ML model...\n")

    retrain()


total_python = 0
total_cpp = 0
total_rust = 0
total_java = 0


for python_file in files:

    print("\n=================================")
    print("Analyzing:", python_file)
    print("=================================")

    with open(python_file, "r", encoding="utf-8") as f:
        python_code = f.read()

    # -------------------------
    # Build IR
    # -------------------------

    ast_tree = ast.parse(python_code)

    ir_program = build_ir(ast_tree)
    ir_program = optimize_ir(ir_program)

    # -------------------------
    # Feature Extraction
    # -------------------------

    features = extract_features(ir_program)

    # -------------------------
    # Static Analysis
    # -------------------------

    space_complexity = analyze_space(ir_program)

    complexity = analyze_complexity(ir_program)

    patterns = detect_patterns(ir_program)

    suggestions = suggest_optimizations(patterns)

    print("\nAI Analysis")
    print("-----------")

    if not patterns:
        print("No patterns detected.")

    for p in patterns:

        print("Pattern:", p["pattern"])
        print("Time Complexity:", p["complexity"])
        print("Space Complexity:", space_complexity)
        print("Suggestion:", p["suggestion"])
        print()

    print("\nAI Optimization Suggestions")
    print("---------------------------")

    for s in suggestions:

        print("Suggestion:", s["message"])
        print("Improvement:", s["improvement"])
        print("Expected Complexity:", s["new_complexity"])
        print()

    # -------------------------
    # AI Optimization
    # -------------------------

    choice = input("\nEnable AI Auto Optimization Learning? (y/n): ").lower()

    if choice == "y":

        print("\nExploring optimizations...\n")

        best_opt = explore(ir_program)

        print("Best optimization discovered:", best_opt)

        store_training_example(features, best_opt)

        retrain()

        ir_program = ai_select(ir_program)

        print("AI optimization applied.")

    else:

        print("Skipping ML optimization.")

    base = os.path.basename(python_file).replace(".py", "")

    cpp_path = f"generated/{base}.cpp"
    rust_path = f"generated/{base}.rs"
    java_path = "generated/GeneratedProgram.java"

    # -------------------------
    # Generate Code
    # -------------------------

    cpp_code = generate_cpp(ir_program)

    with open(cpp_path, "w") as f:
        f.write(cpp_code)

    rust_code = generate_rust(ir_program)

    create_rust_project(rust_code)

    with open(rust_path, "w") as f:
        f.write(rust_code)

    java_code = generate_java(ir_program)

    with open(java_path, "w") as f:
        f.write(java_code)

    # -------------------------
    # Compile Programs
    # -------------------------

    if compile_cpp(cpp_path, "generated/cpp_program"):
        cpp_time = run_cpp("./generated/cpp_program")
    else:
        cpp_time = float("inf")

    if compile_rust("generated"):
        rust_time = run_rust()
    else:
        rust_time = float("inf")

    if compile_java(java_path):
        java_time = run_java()
    else:
        java_time = float("inf")

    py_time = run_python(python_file)

    # -------------------------
    # Performance Comparison
    # -------------------------

    print("\nPerformance Comparison")
    print("----------------------")

    print("Python:", py_time)
    print("C++:", cpp_time)
    print("Rust:", rust_time)
    print("Java:", java_time)

    fastest = min(py_time, cpp_time, rust_time, java_time)

    if fastest == cpp_time:
        print("Fastest language: C++ 🚀")

    elif fastest == rust_time:
        print("Fastest language: Rust 🚀")

    elif fastest == java_time:
        print("Fastest language: Java 🚀")

    else:
        print("Fastest language: Python")

    if cpp_time != 0:
        print("C++ speedup:", round(py_time / cpp_time, 2), "x")

    if rust_time != 0:
        print("Rust speedup:", round(py_time / rust_time, 2), "x")

    if java_time != 0:
        print("Java speedup:", round(py_time / java_time, 2), "x")

    total_python += py_time
    total_cpp += cpp_time
    total_rust += rust_time
    total_java += java_time

    generate_report(patterns, complexity, py_time, cpp_time, rust_time)

    plot_performance(py_time, cpp_time, rust_time, java_time)


print("\n==============================")
print("Project Performance Summary")
print("==============================")

print("Total Python time:", total_python)
print("Total C++ time:", total_cpp)
print("Total Rust time:", total_rust)
print("Total Java time:", total_java)
