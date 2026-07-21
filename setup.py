"""
SCOS Package Setup
Install with: pip install -e .
"""

from setuptools import setup, find_packages

setup(
    name="scos",
    version="1.0.0",
    description="Self-Conscious Operating System - Physical Consensus Architecture",
    long_description="""
SCOS (Self-Conscious Operating System) establishes trust through 
physical consensus rather than institutional authority. The kernel 
serves as a genesis block in an immutable chain of witnessed 
state transitions.
    """,
    long_description_content_type="text/markdown",
    author="SCOS Network Witnesses",
    url="https://github.com/YOUR_USERNAME/scos",
    packages=find_packages(),
    install_requires=[
        'psutil>=5.8.0',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Security :: Cryptography",
        "Topic :: System :: Distributed Computing",
    ],
    python_requires='>=3.8',
)
