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
        "numpy",
        "gymnasium",
        "torch",
        "click",
    ],
    python_requires=">=3.13",
)
