
import random
import ast

from compiler.frontend.ast_to_ir import build_ir
from compiler.ai.feature_extractor import extract_features
from compiler.ai.learning_engine import store_training_example
from compiler.ai.explore_optimizations import explore


def build_dataset(samples=200):

    print("Generating synthetic training programs...")

    for _ in range(samples):

        program_type = random.choice([
            "summation",
            "nested",
            "vector_add",
            "vector_scale",
            "formula",
            "map_loop"
        ])

        n = random.randint(1000, 1000000)

        if program_type == "summation":

            code = f"""
total = 0
for i in range({n}):
    total += i
print(total)
"""

        elif program_type == "nested":

            code = f"""
total = 0
for i in range({n//100}):
    for j in range({n//100}):
        total += i + j
print(total)
"""

        elif program_type == "vector_add":

            code = f"""
N = {n}
a = [0]*N
b = [0]*N
c = [0]*N

for i in range(N):
    c[i] = a[i] + b[i]

print(c[0])
"""

        elif program_type == "vector_scale":

            code = f"""
N = {n}
a = [0]*N

for i in range(N):
    a[i] = a[i] * 2

print(a[0])
"""

        elif program_type == "formula":

            code = f"""
n = {n}
total = n*(n-1)//2
print(total)
"""

        elif program_type == "map_loop":

            code = f"""
N = {n}
a = [0]*N
b = [0]*N

for i in range(N):
    b[i] = a[i] + 1

print(b[0])
"""

        # -----------------------------
        # Convert code -> AST
        # -----------------------------

        tree = ast.parse(code)

        # -----------------------------
        # AST -> IR
        # -----------------------------

        ir = build_ir(tree)

        # -----------------------------
        # Extract features
        # -----------------------------

        features = extract_features(ir)

        # -----------------------------
        # Explore optimizations
        # -----------------------------

        best = explore(ir)

        # -----------------------------
        # Store training example
        # -----------------------------

        store_training_example(features, best)

    print("Dataset generation complete")
