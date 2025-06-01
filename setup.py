"""
Setup configuration for Octopus Energy Agile Pricing Data Fetcher.

Copyright (c) 2025 Gavin Morrison
Licensed under the MIT License. See LICENSE file for details.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="octopus-agile-pricing",
    version="1.0.0",
    author="Gavin Morrison",
    description="A Python script to fetch and analyze Octopus Energy Agile pricing data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gavinmorrison/octopus-agile-pricing",
    py_modules=["octopus_agile_prices"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Utilities",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    keywords="octopus energy agile pricing electricity tariff uk",
    project_urls={
        "Bug Reports": "https://github.com/gavinmorrison/octopus-agile-pricing/issues",
        "Source": "https://github.com/gavinmorrison/octopus-agile-pricing",
    },
)
