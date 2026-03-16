# AI-Compiler
AI Compiler is a project I built to explore a simple but exciting idea:
Can I make a compiler that does not just translate code, but also learns how to optimize it better over time?
This project takes Python code, analyzes it, converts it into an internal representation, applies optimization passes, and then generates backend code in languages like C++, Rust, and Java. On top of that, it also benchmarks the generated versions and uses the results as feedback for future optimization choices.
So in a way, this project sits between a traditional compiler, a performance experimentation tool, and a small research prototype.

# What this project does
At a high level, the pipeline looks like this:

Python → AST → IR → Optimization Passes → Backend Codegen → Benchmarking → ML Feedback

The system currently focuses mostly on loop-heavy and computation-oriented Python programs. It can inspect the structure of a program, estimate complexity, detect patterns like linear iteration, and try different optimization strategies such as:

>constant folding

>loop optimization

>vectorization

>loop tiling

>parallelization experiments

>backend code generation for C++, Rust, and Java

>benchmarking generated outputs

>ML-guided optimization selection

The long-term idea is to make the compiler smarter over time by learning which optimizations work best for certain code patterns.

# Why I made this
I wanted to build something that is more than a normal “toy compiler.”
A lot of compiler projects are great for learning parsing, ASTs, and code generation, but I wanted to push it further into something that feels more modern and research-oriented. I was especially interested in combining three things in one project:

>compiler construction

>performance optimization

>machine learning feedback

This project became my way of experimenting with all three together.

# Main idea
Traditional compilers usually apply optimization passes based on fixed rules.
In this project, I wanted to explore something more dynamic:

>analyze the Python program

>generate an internal representation

>try multiple optimization candidates

>benchmark them

>collect the result

>let ML help choose better optimizations later

So instead of hardcoding every decision forever, the compiler can gradually build experience from data.
That is the main concept behind AI Compiler.

# Current features
Right now, the project includes:

>Python parsing using AST

>AST to IR conversion

>optimization pipeline

>feature extraction for ML

>synthetic dataset generation

>automatic benchmarking

>complexity analysis

>performance reporting

>backend generation for:

>C++

>Rust

>Java

>CLI-based workflow

It is still an experimental project, but it already works well as a learning platform and as a prototype for future compiler research ideas.

# How it works
1. Parsing Python:
The compiler starts by reading a Python file and building its AST using Python’s built-in ast module.

2. Building IR:
The AST is converted into a simpler intermediate representation. This IR is easier to analyze and transform than raw Python syntax.

3. Optimization passes:
Once the IR is built, the compiler applies optimization passes such as constant folding, loop transformations, vectorization, and tiling.

4. AI-guided exploration:
The project can generate different optimization candidates and benchmark them to see which one performs best.

5. ML feedback:
The results of those experiments can be stored as training data so the model can later predict better optimization choices.

6. Backend generation:
The optimized IR can then be emitted as C++, Rust, or Java code.

7. Benchmarking:
The generated versions are compiled and timed, and the final output shows performance comparisons and speedups.

# Example workflow
A typical run looks like this:

BASH: python main.py

Then the tool may ask for:

Enter Python file or project folder: test.py
Generate synthetic training data? (y/n): y

After that, the pipeline can:

>analyze the source

>run optimization passes

>explore candidate optimizations

>benchmark versions

>retrain the ML model

>generate backend code

>compare performance across languages

# Installation
Clone the repository first:

BASH: git clone https://github.com/your-username/ai-compiler.git
      cd ai-compiler

Install dependencies:

BASH: pip install -r requirements.txt

Depending on which backends you want to use, you may also need:

>g++ for C++

>Rust + Cargo for Rust

>Java JDK for Java

>Requirements

This project mainly uses Python, but backend benchmarking depends on external compilers too.
You should ideally have:

>Python 3.10+

>pip

>g++

>Rust toolchain

>Java JDK

If you only want to study the frontend and optimizer pipeline, Python alone is enough for much of the project.

# How to use it

# Analyze a Python file

BASH: python main.py

Then provide a .py file when prompted.
# Generate synthetic training data
When asked:
Generate synthetic training data? (y/n): y

the compiler can create extra training examples for the ML side of the project.

# Benchmark generated backends
If the C++, Rust, and Java toolchains are installed, the compiler can compile generated code and compare runtime performance automatically.

# Learning value of this project
One thing I really like about this project is that it is useful even if someone is not using it as a production tool.
This repo can also be used as a learning resource for:

>compiler basics

>AST handling in Python

>intermediate representations

>optimization passes

>backend code generation

>benchmarking workflows

>feature engineering for ML

>feedback-driven optimization research

So even if someone only wants to understand how compilers work internally, this project can still be helpful.

# What this project currently handles well
Right now, the compiler is best suited for:

>loop-heavy Python programs

>arithmetic-heavy code

>simple structured control flow

>performance experiments

>learning and research use

It works best when the input program is relatively straightforward and computation-focused.

# Current limitations
This is still an experimental project, so there are some important limitations.
Right now, it does not fully support:

>the full Python language

>advanced Python libraries

>complex object-oriented behavior

>dynamic runtime-heavy features

>arbitrary third-party APIs

>complete semantic equivalence for all Python programs

The ML part is also still in an early stage. It is useful as an experimental decision layer, but it is not yet a large-scale intelligent model. At the moment, it helps most as a prototype for optimization selection rather than as a magical all-knowing optimizer.
I think being honest about this is important, because the project is strongest as a research and learning system, not as a drop-in replacement for Python execution.

# Why the ML part matters
A fair question is: does the ML actually help?
The answer right now is: yes, but in a limited and experimental way.
The ML system helps by:

>extracting features from programs

>storing optimization outcomes

>learning from benchmark results

>selecting candidate optimizations based on past examples

So it does add value, but the bigger value today is in the framework it creates for future autotuning and learning-based optimization.
The exciting part is not just the current accuracy — it is the direction.

# Future improvements
There is still a lot I want to improve. Some of the next big directions are:

>stronger complexity analysis

>better loop dependence analysis

>more reliable vectorization

>stronger autotuning

>profile-guided optimization

>richer Python subset support

>better IR design

>deeper ML feedback loop

>smarter backend generation

>improved CLI experience

>better error handling and diagnostics

This project has a lot of room to grow, and that is part of what makes it interesting.

# Research potential
I also believe this project has strong research potential.
Possible research directions include:

>ML-guided compiler optimization

>feedback-driven autotuning

>optimization selection from static features

>hybrid compiler design

>educational compiler frameworks

>complexity-aware optimization systems

So this repo is not just code — it can also become the basis for a paper, project report, or deeper experimentation.

# For students and learners
If you are learning compilers, I recommend exploring the project in this order:

>start with AST parsing

>understand the IR

>study the optimizer pipeline

>look at the feature extractor

>inspect candidate generation

>review backend codegen

>check the benchmarking system

>then study how ML feedback is integrated

That path makes the whole project much easier to understand.

# Example goals for contributors or learners
Some good ways to extend this project are:

>add support for more Python constructs

>improve IR expressiveness

>build new optimization passes

>strengthen backend output quality

>add tests and validation

>improve the ML model and dataset design

>add profile-guided or hardware-aware optimizations

>make the CLI even more polished

# Disclaimer
This project is experimental and intended mainly for:

>learning

>research

>prototyping

>performance exploration

It should not yet be treated as a complete production-grade Python compiler.

# License
This project is licensed under the MIT License.

# Final note
I built this project because I wanted to experiment with the idea that a compiler can be more than a translator. It can be something that analyzes, experiments, learns, and improves.
That is what AI Compiler is trying to become.
If you check out this repo, I hope it helps you learn something new about compilers, optimization, or ML-guided systems.
