import time
import subprocess

def run_python(file):

    start = time.time()

    subprocess.run(["python3", file])

    end = time.time()

    return end - start


def run_cpp(executable):

    start = time.time()

    subprocess.run([executable], check=True)

    end = time.time()

    return end - start
