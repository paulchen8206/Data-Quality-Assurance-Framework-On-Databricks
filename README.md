# QA Framework

[![CI/CD](https://github.com/paulchen8206/Qa-Framework-On-Databricks/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/paulchen8206/Qa-Framework-On-Databricks/actions/workflows/ci-cd.yml)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![Status](https://img.shields.io/badge/status-validated-success.svg)](./docs/validation_report.md)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A production-ready Databricks bundle project for data quality assurance with Python. Features both lightweight validators for quick checks and comprehensive Great Expectations integration for advanced data quality pipelines.

## ✨ Key Features

- **Dual Validation Approach**: Choose lightweight validators or comprehensive Great Expectations
- **50+ Built-in Expectations**: Statistical validations, pattern matching, and data profiling
- **Databricks Optimized**: Native PySpark integration for big data workflows
- **Production Ready**: Fully tested with CI/CD pipeline support
- **Easy Deployment**: Databricks bundle configuration for dev/prod environments

## 📋 Table of Contents

- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Build and Wheel](#build-and-wheel)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Testing](#-testing)
- [Deployment](#-deployment)
- [Development](#-development)
- [Troubleshooting](#-troubleshooting)
- [Resources](#-resources)

## 🚀 Quick Start

```bash
# 1. Clone and navigate to the project
cd /path/to/Qa-Framework

# 2. Sync dependencies (creates and manages .venv)
uv sync --all-groups

# 3. Install package with dependencies
uv sync --all-groups

# 4. Run tests
uv run pytest tests/test_utils.py -v

# 5. Try the DataValidator
uv run python -c "from qa_framework import DataValidator; print('✓ Ready!')"
```

## 📦 Installation

### Prerequisites

- **Python**: 3.11
- **Java**: Required for PySpark (JDK 8 or 11)
- **Databricks CLI**: For bundle deployment

### Using uv (Recommended)

[uv](https://github.com/astral-sh/uv) is a fast Python package installer.

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install all dependency groups (dev is default)
uv sync --all-groups
```

## Build and Wheel

Use the included `Makefile` to build and validate wheel artifacts locally.

### 1. Build the wheel

```bash
make build-wheel
```

This creates artifacts in `dist/`:

- `qa_framework-<version>-py3-none-any.whl`
- `qa_framework-<version>.tar.gz`

### 2. Verify package metadata

```bash
make check-wheel
```

### 3. Install the built wheel

```bash
make install-wheel
```

### 4. Smoke test installed wheel

```bash
make smoke-wheel
```

Expected output:

```text
wheel import OK
```

### 5. Use the installed package

```bash
python -c "from qa_framework import DataValidator, GreatExpectationsValidator; print(DataValidator, GreatExpectationsValidator)"
```

If you prefer plain commands (without `make`):

```bash
uv sync --all-groups
uv build
uvx twine check dist/*
uv pip install --force-reinstall dist/qa_framework-*.whl
```

### Databricks Configuration

1. Install Databricks CLI:
   ```bash
    uv tool install databricks-cli
   ```

2. Configure authentication:
   ```bash
   databricks configure --token
   ```

3. Update [databricks.yml](databricks.yml) with your workspace URL

## 🎯 Usage

### DataValidator (Quick & Simple)

Perfect for ad-hoc validations and quick checks:

```python
from qa_framework import DataValidator
from pyspark.sql import SparkSession

# Initialize Spark
spark = SparkSession.builder.appName("QA").getOrCreate()

# Load your data
df = spark.read.parquet("path/to/data.parquet")

# Create validator
validator = DataValidator(df)

# Run validations
validator.check_null_values()
validator.check_duplicates()
validator.check_value_range("age", min_value=0, max_value=120)
validator.check_column_exists("user_id")

# Get summary report
summary = validator.get_validation_summary()
print(summary)
```

### GreatExpectationsValidator (Comprehensive)

For production data quality pipelines with advanced features:

```python
from qa_framework import GreatExpectationsValidator

# Create validator
ge_validator = GreatExpectationsValidator(
    df, 
    expectation_suite_name="production_suite"
)

# Table-level expectations
ge_validator.expect_table_row_count_to_be_between(
    min_value=100, 
    max_value=1000000
)

# Column-level validations
ge_validator.expect_column_values_to_not_be_null("user_id")
ge_validator.expect_column_values_to_be_unique("transaction_id")
ge_validator.expect_column_values_to_be_in_set(
    "status", 
    ["active", "inactive", "pending"]
)

# Pattern matching
ge_validator.expect_column_values_to_match_regex(
    "email", 
    r"^[\w\.-]+@[\w\.-]+\.\w+$"
)

# Statistical checks
ge_validator.expect_column_mean_to_be_between(
    "amount", 
    min_value=10, 
    max_value=1000
)

# Validate and get results
results = ge_validator.validate()
summary = ge_validator.get_validation_summary()

# Save suite for reuse
ge_validator.save_expectation_suite()
```

### Examples

See complete working examples:

- [run_tests.py](code/notebooks/run_tests.py) - DataValidator examples
- [run_ge_tests.py](code/notebooks/run_ge_tests.py) - Great Expectations with e-commerce data

## 📁 Project Structure

```text
Qa-Framework/
├── databricks.yml              # Bundle configuration
├── pyproject.toml              # Modern Python project config
├── uv.lock                     # Locked dependencies for reproducible builds
├── readme.md                   # This file
├── docs/                       # Project documentation
│   ├── validation_report.md    # Validation status
│   └── contributing.md         # Contribution guide
│
├── code/                      
│   ├── qa_framework/           # Main package
│   │   ├── __init__.py         # Package exports
│   │   ├── validators.py       # DataValidator class
│   │   ├── ge_validator.py     # Great Expectations integration
│   │   └── utils.py            # Helper functions
│   └── notebooks/              # Databricks notebooks
│       ├── run_tests.py        # DataValidator examples
│       └── run_ge_tests.py     # Great Expectations examples
│
├── tests/                      # Test suite
│   ├── conftest.py             # Pytest fixtures
│   ├── test_validators.py      # Validator tests
│   ├── test_utils.py           # Utility tests
│   └── test_ge_validator.py    # GE tests
│
├── great_expectations/         # GE configuration
│   ├── great_expectations.yml  # GE config
│   ├── expectations/           # Expectation suites
│   ├── checkpoints/            # Validation checkpoints
│   └── plugins/                # Custom expectations
│
├── environments/               # Environment configs
│   ├── dev.yml                 # Dev settings
│   └── prod.yml                # Prod settings
│
└── resources/                  # Job definitions
    ├── qa_test_job.yml         # DataValidator job
    └── qa_ge_test_job.yml      # GE job
```

## 🧪 Testing

### Run Tests Locally

```bash
# Run all tests
uv run pytest

# Run specific test file
uv run pytest tests/test_utils.py -v

# Run with coverage
uv run pytest --cov=qa_framework --cov-report=html

# Run only fast tests (skip PySpark tests)
uv run pytest tests/test_utils.py -v
```

### Test Categories

- **Utils Tests** (`test_utils.py`): Fast, no PySpark required ✓
- **Validator Tests** (`test_validators.py`): Require PySpark/Java setup
- **GE Tests** (`test_ge_validator.py`): Slow due to GE dependencies (~20-30s)

### Note on PySpark Tests

PySpark tests require Java and proper Spark setup. On Databricks, all tests run successfully. For local development:

- Utils tests run without special setup
- Validator tests need Java 8 or 11 installed
- Use Databricks for full integration testing

## 🚢 Deployment

### Validate Bundle

```bash
# Check bundle configuration
databricks bundle validate
```

### Deploy to Environment

```bash
# Deploy to development
databricks bundle deploy -t dev

# Deploy to production
databricks bundle deploy -t prod
```

### Run Jobs

```bash
# Run DataValidator job
databricks bundle run qa_test_job -t dev

# Run Great Expectations job  
databricks bundle run qa_ge_test_job -t dev
```

### Deployment Workflow

1. **Local Development**
   - Make changes locally
    - Run unit tests: `uv run pytest tests/test_utils.py`
    - Test import: `uv run python -c "from qa_framework import DataValidator"`

2. **Dev Environment**
   - Deploy: `databricks bundle deploy -t dev`
   - Run validation jobs
   - Verify results in workspace

3. **Production**
   - Deploy: `databricks bundle deploy -t prod`
   - Monitor job runs
   - Set up alerts for failures

## 👨‍💻 Development

### Development Workflow

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/new-validator
   ```

2. **Make Changes**
   - Write code in `code/qa_framework/`
   - Add tests in `tests/`
   - Update documentation

3. **Test Locally**
    ```bash
    uv run pytest tests/test_utils.py -v
    uv run python -c "from qa_framework import DataValidator"
    ```

4. **Deploy to Dev**
    ```bash
    databricks bundle deploy -t dev
    databricks bundle run qa_test_job -t dev
    ```

5. **Create Pull Request**
    - Ensure tests pass
    - Update [docs/validation_report.md](docs/validation_report.md) if needed
    - Request review

### Adding New Validators

```python
# In code/qa_framework/validators.py
def check_new_validation(self, column: str) -> bool:
    """
    Add your validation logic here
    
    Args:
        column: Column to validate
        
    Returns:
        True if validation passes
    """
    # Validation logic
    result = self.df.filter(col(column).isNotNull()).count() > 0
    
    # Record result
    self.validation_results.append({
        "check": "new_validation",
        "column": column,
        "passed": result
    })
    
    return result
```

### Adding New Great Expectations

```python
# In code/qa_framework/ge_validator.py
def expect_custom_validation(
    self, 
    column: str, 
    **kwargs
) -> Dict[str, Any]:
    """
    Custom expectation wrapper
    
    Args:
        column: Column name
        **kwargs: Additional parameters
        
    Returns:
        Validation result
    """
    return self.validator.expect_column_custom_validation(
        column,
        **kwargs
    )
```

## 🔧 Troubleshooting

### Import Errors

```bash
# Reinstall in editable mode
uv sync --all-groups
```

### PySpark Test Failures

Ensure Java is installed:
```bash
# Check Java version
java -version

# Should show Java 8 or 11
```

### Great Expectations Slow Performance

This is expected. GE has heavy dependencies (pandas, numpy, pyspark). Initial import takes 20-30 seconds.

### Bundle Validation Errors

```bash
# Check YAML syntax
databricks bundle validate

# Verify workspace URL
cat databricks.yml | grep workspace_url
```

## ✅ Validation

See [docs/validation_report.md](docs/validation_report.md) for:
- Complete validation status
- Known issues and notes
- Test results
- Recommendations

### Quick Validation Check

```bash
# Verify installation
uv run python -c "from qa_framework import DataValidator, GreatExpectationsValidator; print('✓ Installation OK')"

# Run fast tests
uv run pytest tests/test_utils.py -v

# Check package details
uv pip show qa_framework
```

## 📚 Resources

- [Great Expectations Documentation](https://docs.greatexpectations.io/)
- [Databricks Bundles Guide](https://docs.databricks.com/dev-tools/bundles/)
- [PySpark Documentation](https://spark.apache.org/docs/latest/api/python/)

## 🤝 Contributing

We welcome contributions! Please see [docs/contributing.md](docs/contributing.md) for detailed guidelines on:

- Setting up the development environment
- Coding standards and best practices
- Testing requirements
- Submitting pull requests

Quick contribution steps:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes with tests
4. Commit your changes (`git commit -m 'feat: Add amazing feature'`)
5. Push to your fork (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Copyright (c) 2026 Paul Chen

---

**Project Status**: ✅ Validated and Ready for Production  
**Last Validated**: March 7, 2026  
**Python Version**: 3.11  
**Databricks Runtime**: Compatible with DBR 13.0+
