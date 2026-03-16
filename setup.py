from setuptools import setup, find_packages

setup(
    name="ai-python-compiler",
    version="0.1.0",
    description="AI Self-Learning Python Compiler",
    author="Your Name",
    packages=find_packages(),
    install_requires=[
        "rich",
        "numpy",
        "scikit-learn",
        "matplotlib"
    ],
    entry_points={
        "console_scripts": [
            "aicompile=compiler.cli:main",
        ],
    },
)
