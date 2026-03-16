import random

def generate_program():

    n = random.choice([10000, 50000, 100000, 1000000])

    program_type = random.choice([
        "sum_loop",
        "nested_loop",
        "simple_loop"
    ])

    if program_type == "sum_loop":

        return f"""
total = 0
for i in range({n}):
    total += i
print(total)
"""

    if program_type == "nested_loop":

        return f"""
total = 0
for i in range(1000):
    for j in range(100):
        total += i*j
print(total)
"""

    if program_type == "simple_loop":

        return f"""
x = 0
for i in range({n}):
    x = x + 1
print(x)
"""
