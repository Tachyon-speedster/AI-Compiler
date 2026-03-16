import argparse
import ast
import os

from rich.console import Console
from rich.table import Table
from rich.progress import Progress
from rich.panel import Panel

from compiler.frontend.ast_to_ir import build_ir
from compiler.optimizer.optimizer_pipeline import optimize_ir

from compiler.backend.cpp_backend import generate_cpp
from compiler.backend.rust_backend import generate_rust, create_rust_project
from compiler.backend.java_backend import generate_java

from compiler.runtime.runner import (
    compile_cpp,
    compile_rust,
    compile_java,
    run_cpp,
    run_rust,
    run_java
)

from compiler.runtime.benchmark import run_python

from compiler.analysis.pattern_detector import detect_patterns
from compiler.analysis.complexity_analyzer import analyze_complexity
from compiler.analysis.space_analyzer import analyze_space

from compiler.ai.ai_optimizer import ai_select
from compiler.ai.auto_dataset_builder import build_dataset
from compiler.ai.auto_train import retrain


console = Console()


# ---------------------------------------------------
# CLI Header
# ---------------------------------------------------

def header():

    console.print(
        Panel.fit(
            "[bold cyan]AI Self-Learning Python Compiler[/bold cyan]\n"
            "[dim]Python → IR → AI Optimization → Native Code[/dim]",
            border_style="cyan"
        )
    )


# ---------------------------------------------------
# Compile
# ---------------------------------------------------

def compile_program(file):

    header()

    with Progress() as progress:

        task = progress.add_task("[cyan]Compiler Pipeline", total=5)

        progress.update(task, advance=1, description="Parsing Python")

        with open(file) as f:
            code = f.read()

        tree = ast.parse(code)

        progress.update(task, advance=1, description="Building IR")

        ir = build_ir(tree)

        progress.update(task, advance=1, description="Running Optimizer")

        ir = optimize_ir(ir)
        ir = ai_select(ir)

        progress.update(task, advance=1, description="Generating Code")

        os.makedirs("generated", exist_ok=True)

        base = os.path.basename(file).replace(".py", "")

        cpp_path = f"generated/{base}.cpp"
        rust_path = f"generated/{base}.rs"
        java_path = "generated/GeneratedProgram.java"

        cpp_code = generate_cpp(ir)
        rust_code = generate_rust(ir)
        java_code = generate_java(ir)

        with open(cpp_path, "w") as f:
            f.write(cpp_code)

        with open(rust_path, "w") as f:
            f.write(rust_code)

        with open(java_path, "w") as f:
            f.write(java_code)

        create_rust_project(rust_code)

        progress.update(task, advance=1, description="Finished")

    console.print("\n[bold green]✔ Compilation complete[/bold green]")
    console.print(f"[dim]Generated files in: generated/[/dim]")


# ---------------------------------------------------
# Analyze
# ---------------------------------------------------

def analyze_program(file):

    header()

    with open(file) as f:
        code = f.read()

    tree = ast.parse(code)

    ir = build_ir(tree)

    patterns = detect_patterns(ir)
    complexity = analyze_complexity(ir)
    space = analyze_space(ir)

    table = Table(title="Program Analysis")

    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Time Complexity", complexity)
    table.add_row("Space Complexity", space)

    console.print(table)

    if patterns:

        ptable = Table(title="Detected Patterns")

        ptable.add_column("Pattern")
        ptable.add_column("Suggestion")

        for p in patterns:

            ptable.add_row(
                p["pattern"],
                p["suggestion"]
            )

        console.print(ptable)

    else:

        console.print("[yellow]No patterns detected[/yellow]")


# ---------------------------------------------------
# Benchmark
# ---------------------------------------------------

def benchmark_program(file):

    header()

    base = os.path.basename(file).replace(".py", "")
    cpp_path = f"generated/{base}.cpp"

    if not os.path.exists(cpp_path):

        console.print(
            "[yellow]Compiled output not found. Compiling first...[/yellow]"
        )

        compile_program(file)

    console.print("\n[bold]Running Benchmarks[/bold]\n")

    py_time = run_python(file)

    cpp_time = float("inf")
    rust_time = float("inf")
    java_time = float("inf")

    if compile_cpp(cpp_path, "generated/cpp_program"):
        cpp_time = run_cpp("./generated/cpp_program")

    if compile_rust("generated"):
        rust_time = run_rust()

    if compile_java("generated/GeneratedProgram.java"):
        java_time = run_java()

    table = Table(title="Benchmark Results")

    table.add_column("Language", style="cyan")
    table.add_column("Execution Time (s)", style="green")

    table.add_row("Python", str(py_time))
    table.add_row("C++", str(cpp_time))
    table.add_row("Rust", str(rust_time))
    table.add_row("Java", str(java_time))

    console.print(table)

    fastest = min(py_time, cpp_time, rust_time, java_time)

    if fastest == rust_time:
        console.print("[bold green]🚀 Rust is fastest[/bold green]")

    elif fastest == cpp_time:
        console.print("[bold green]🚀 C++ is fastest[/bold green]")

    elif fastest == java_time:
        console.print("[bold green]🚀 Java is fastest[/bold green]")

    else:
        console.print("[yellow]Python is fastest (unexpected)[/yellow]")


# ---------------------------------------------------
# Train AI
# ---------------------------------------------------

def train_model():

    header()

    console.print("[bold]Generating synthetic dataset...[/bold]")

    build_dataset(100)

    console.print("[bold]Training ML model...[/bold]")

    retrain()

    console.print("[bold green]✔ Training complete[/bold green]")


# ---------------------------------------------------
# CLI
# ---------------------------------------------------

def main():

    parser = argparse.ArgumentParser(
        prog="aicompile",
        description="AI Self-Learning Python Compiler"
    )

    sub = parser.add_subparsers(dest="command")

    compile_cmd = sub.add_parser("compile", help="compile python program")
    compile_cmd.add_argument("file")

    analyze_cmd = sub.add_parser("analyze", help="analyze program")
    analyze_cmd.add_argument("file")

    bench_cmd = sub.add_parser("benchmark", help="benchmark compiled program")
    bench_cmd.add_argument("file")

    sub.add_parser("train", help="train optimization model")

    args = parser.parse_args()

    if args.command == "compile":

        compile_program(args.file)

    elif args.command == "analyze":

        analyze_program(args.file)

    elif args.command == "benchmark":

        benchmark_program(args.file)

    elif args.command == "train":

        train_model()

    else:

        parser.print_help()


if __name__ == "__main__":

    main()
