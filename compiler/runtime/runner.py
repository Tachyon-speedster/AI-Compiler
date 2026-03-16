import subprocess
import time
import os


def run_command(cmd):

    try:

        subprocess.check_call(cmd, shell=True)

        return True

    except subprocess.CalledProcessError:

        return False


# -------------------------
# C++
# -------------------------

def compile_cpp(source, output):

    cmd = f"g++ {source} -O3 -march=native -mavx2 -fopenmp -o {output}"

    return run_command(cmd)


def run_cpp(executable):

    start = time.time()

    subprocess.call(executable, shell=True)

    return time.time() - start


# -------------------------
# Rust
# -------------------------

def compile_rust(folder):

    cmd = f"cd {folder} && cargo build --release"

    return run_command(cmd)


def run_rust():

    start = time.time()

    subprocess.call("./generated/target/release/generated", shell=True)

    return time.time() - start


# -------------------------
# Java
# -------------------------

def compile_java(source):

    cmd = f"javac {source}"

    return run_command(cmd)


def run_java():

    start = time.time()

    subprocess.call("java -cp generated GeneratedProgram", shell=True)

    return time.time() - start
