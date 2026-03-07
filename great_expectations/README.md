# Great Expectations Directory

This directory contains Great Expectations configuration and artifacts.

## Structure

```
great_expectations/
├── great_expectations.yml    # Main configuration file
├── expectations/             # Expectation suites (JSON files)
├── checkpoints/              # Checkpoint configurations
├── plugins/                  # Custom expectations and plugins
└── uncommitted/              # Local artifacts (not committed to git)
    ├── data_docs/           # Generated data documentation
    └── validations/         # Validation results
```

## Usage

The Great Expectations context is initialized automatically when using the `GreatExpectationsValidator` class from `qa_framework.ge_validator`.

### Quick Start

```python
from pyspark.sql import SparkSession
from qa_framework.ge_validator import GreatExpectationsValidator

# Create or load DataFrame
spark = SparkSession.builder.getOrCreate()
df = spark.read.parquet("data/my_data.parquet")

# Initialize validator
ge_validator = GreatExpectationsValidator(df, expectation_suite_name="my_suite")

# Add expectations
ge_validator.expect_table_row_count_to_be_between(min_value=100, max_value=10000)
ge_validator.expect_column_values_to_not_be_null("id")
ge_validator.expect_column_values_to_be_unique("id")

# Validate
results = ge_validator.validate()
print(results)
```

## Configuration

The `great_expectations.yml` file can be customized for your environment. By default, it uses:
- File-based stores for expectation suites and validations
- Local data docs site
- No remote storage backends

## Data Docs

To view interactive data quality reports:

```bash
great_expectations docs build
great_expectations docs open
```
