from setuptools import find_packages, setup

setup(
    name="dprl",
    version="0.1.0",
    description="Deep Reinforcement Learning Toolkit",
    author="Lucas Gandara",
    author_email="lucas.gandara@outlook.com",
    url="https://github.com/LucasGandara/dprl",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "click>=8.0.0",
        "numpy>=1.24.0",
        "torch>=2.0.0",
        "gymnasium[classic-control]>=0.29.0",
        "pyyaml>=6.0",
    ],
    python_requires=">=3.13",
)
