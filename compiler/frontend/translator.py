import re

def python_to_cpp(python_code):

    cpp_code = """
#include <iostream>
using namespace std;

int main(){
"""

    lines = python_code.split("\n")
    prints = []
    open_blocks = 0

    for line in lines:

        line = line.strip()

        if line == "":
            continue

        # += operations
        if "+=" in line:
            cpp_code += line + ";\n"

        # variable declaration
        elif "=" in line and "for" not in line:
            var, value = line.split("=")
            var = var.strip()
            value = value.strip()
            cpp_code += f"long long {var} = {value};\n"

        # for loop
        elif "for" in line and "range" in line:

            match = re.search(r"for (.*) in range\((.*)\):", line)

            if match:
                var = match.group(1)
                limit = match.group(2)

                cpp_code += f"""
for(long long {var}=0; {var}<{limit}; {var}++){{
"""
                open_blocks += 1

        # store print statements to add later
        elif line.startswith("print("):
            content = line[6:-1]
            prints.append(f'cout << {content} << endl;')

    # close loops
    for _ in range(open_blocks):
        cpp_code += "}\n"

    # add prints AFTER loops
    for p in prints:
        cpp_code += p + "\n"

    cpp_code += """
return 0;
}
"""

    return cpp_code
