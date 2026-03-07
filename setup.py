from setuptools import setup, find_packages

setup(
    name="qa_framework",
    version="0.1.0",
    description="Data quality assurance framework for Databricks",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(where="code"),
    package_dir={"":"code"},
    python_requires=">=3.8",
    install_requires=[
        "pyspark>=3.4.0",
        "databricks-sdk>=0.18.0",
        "pydantic>=2.0.0",
        "pandas>=2.0.0",
        "pyyaml>=6.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "pytest-mock>=3.11.1",
        ],
    },
)
