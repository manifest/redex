import pathlib
from setuptools import setup
from setuptools import find_packages

README = (pathlib.Path(__file__).parent / "README.md").read_text()

setup(
    name="redex",
    version="0.0.0",
    author="Andrei Nesterov",
    author_email="ae.nesterov@gmail.com",
    url="https://github.com/manifest/redex",
    description="A combinator library for designing algorithms",
    long_description=README,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.9",
        "Topic :: Scientific/Engineering",
        "Typing :: Typed",
    ],
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.9",
    install_requires=[
    ],
    extras_require={
        "docs": ["sphinx", "furo"]
    },
)
