# Databricks notebook source
"""
Great Expectations Example - Advanced Data Quality Validation
"""

# COMMAND ----------

# MAGIC %pip install great-expectations

# COMMAND ----------

import sys
from pathlib import Path

# Add src directory to path
src_path = str(Path(".").absolute().parent)
if src_path not in sys.path:
    sys.path.insert(0, src_path)

# COMMAND ----------

from pyspark.sql import SparkSession
from qa_framework import GreatExpectationsValidator, setup_logger

# Setup logger
logger = setup_logger()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Create Sample Data

# COMMAND ----------

# Create sample e-commerce data
spark = SparkSession.builder.getOrCreate()

sample_data = [
    (1, "user_001", "premium", 150.00, "2024-01-15", "completed"),
    (2, "user_002", "basic", 25.50, "2024-01-16", "completed"),
    (3, "user_003", "premium", 200.00, "2024-01-17", "completed"),
    (4, "user_004", "basic", 15.00, "2024-01-17", "pending"),
    (5, "user_005", "premium", 175.50, "2024-01-18", "completed"),
    (6, "user_006", "basic", 30.00, "2024-01-18", "completed"),
    (7, "user_007", "enterprise", 500.00, "2024-01-19", "completed"),
    (8, "user_008", "basic", 12.50, "2024-01-19", "failed"),
    (9, "user_009", "premium", 180.00, "2024-01-20", "completed"),
    (10, "user_010", "basic", 22.00, "2024-01-20", "completed"),
]

df = spark.createDataFrame(
    sample_data,
    ["transaction_id", "user_id", "tier", "amount", "date", "status"]
)

display(df)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Initialize Great Expectations Validator

# COMMAND ----------

# Create validator with a named expectation suite
ge_validator = GreatExpectationsValidator(
    df=df,
    expectation_suite_name="ecommerce_transactions_suite"
)

logger.info("Initialized Great Expectations validator")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Define Data Quality Expectations

# COMMAND ----------

# Table-level expectations
logger.info("Adding table-level expectations...")

# Expect reasonable number of transactions
result = ge_validator.expect_table_row_count_to_be_between(
    min_value=5,
    max_value=1000000
)
logger.info(f"Row count expectation: {result['success']}")

# COMMAND ----------

# Column existence and completeness expectations
logger.info("Adding column completeness expectations...")

# Transaction ID should never be null and should be unique
ge_validator.expect_column_values_to_not_be_null("transaction_id")
ge_validator.expect_column_values_to_be_unique("transaction_id")

# User ID should never be null
ge_validator.expect_column_values_to_not_be_null("user_id")

# Amount should never be null
ge_validator.expect_column_values_to_not_be_null("amount")

logger.info("Completeness expectations added")

# COMMAND ----------

# Value range and domain expectations
logger.info("Adding value range and domain expectations...")

# Transaction amounts should be positive and reasonable
ge_validator.expect_column_values_to_be_between(
    column="amount",
    min_value=0.01,
    max_value=10000.00,
    mostly=1.0  # 100% of values must be in range
)

# Tier must be one of the allowed values
ge_validator.expect_column_values_to_be_in_set(
    column="tier",
    value_set=["basic", "premium", "enterprise"],
    mostly=1.0
)

# Status must be one of the allowed values
ge_validator.expect_column_values_to_be_in_set(
    column="status",
    value_set=["completed", "pending", "failed", "cancelled"],
    mostly=1.0
)

# Date format validation (YYYY-MM-DD)
ge_validator.expect_column_values_to_match_regex(
    column="date",
    regex=r"^\d{4}-\d{2}-\d{2}$",
    mostly=1.0
)

# User ID format validation (user_XXX)
ge_validator.expect_column_values_to_match_regex(
    column="user_id",
    regex=r"^user_\d{3}$",
    mostly=1.0
)

logger.info("Value range and domain expectations added")

# COMMAND ----------

# Statistical expectations
logger.info("Adding statistical expectations...")

# Average transaction should be between $10 and $300
ge_validator.expect_column_mean_to_be_between(
    column="amount",
    min_value=10.0,
    max_value=300.0
)

logger.info("Statistical expectations added")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Run Validation

# COMMAND ----------

# Execute all expectations
logger.info("Running validation...")
validation_results = ge_validator.validate()

# Display results
logger.info("Validation complete!")
print("\n" + "="*60)
print("VALIDATION RESULTS")
print("="*60)

# Get summary
summary = ge_validator.get_validation_summary()

print(f"\nOverall Success: {summary['success']}")
print(f"Total Expectations: {summary['evaluated_expectations']}")
print(f"Successful: {summary['successful_expectations']}")
print(f"Failed: {summary['unsuccessful_expectations']}")
print(f"Success Rate: {summary['success_percent']:.1f}%")
print("="*60)

# COMMAND ----------

# Display detailed results
print("\nDetailed Results:\n")

for idx, result in enumerate(summary['results'], 1):
    expectation_type = result['expectation_config']['expectation_type']
    success = result['success']
    status_icon = "✓" if success else "✗"
    
    print(f"{idx}. {status_icon} {expectation_type}")
    
    if 'kwargs' in result['expectation_config']:
        kwargs = result['expectation_config']['kwargs']
        if 'column' in kwargs:
            print(f"   Column: {kwargs['column']}")
        
        # Show relevant parameters
        for key in ['min_value', 'max_value', 'value_set', 'regex', 'mostly']:
            if key in kwargs:
                print(f"   {key}: {kwargs[key]}")
    
    if not success and 'result' in result:
        print(f"   Result: {result['result']}")
    
    print()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Save Expectation Suite

# COMMAND ----------

# Save the expectation suite for reuse
ge_validator.save_expectation_suite()
logger.info(f"Saved expectation suite: ecommerce_transactions_suite")

print("\nExpectation suite saved successfully!")
print("You can reuse this suite for future validations.")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Compare with Legacy Validator

# COMMAND ----------

from qa_framework import DataValidator

# Run the same checks with the legacy validator for comparison
legacy_validator = DataValidator(df)

print("Running legacy validation checks...")
print("\n" + "="*60)
print("LEGACY VALIDATOR RESULTS")
print("="*60)

# Check nulls
null_counts = legacy_validator.check_null_values()
print(f"\nNull counts: {null_counts}")

# Check duplicates
dup_count = legacy_validator.check_duplicates()
print(f"Duplicate rows: {dup_count}")

# Check value ranges
amount_range = legacy_validator.check_value_range("amount", min_value=0.01, max_value=10000)
print(f"Amount range violations: {amount_range['violations']}")

# Get summary
legacy_summary = legacy_validator.get_validation_summary()
print(f"\nLegacy validation - Passed: {legacy_summary['passed_checks']}/{legacy_summary['total_checks']}")
print("="*60)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Key Takeaways
# MAGIC 
# MAGIC **Great Expectations provides:**
# MAGIC - Rich expectation library with 50+ built-in expectations
# MAGIC - Statistical validations (mean, median, stddev, etc.)
# MAGIC - Pattern matching and regex validations
# MAGIC - Data documentation and visualization
# MAGIC - Expectation suite reusability
# MAGIC - Integration with data pipelines
# MAGIC 
# MAGIC **Legacy DataValidator provides:**
# MAGIC - Simple, focused validations
# MAGIC - Lightweight and easy to understand
# MAGIC - Quick implementation for basic checks
# MAGIC 
# MAGIC **Recommendation:** Use both!
# MAGIC - Use Great Expectations for comprehensive data quality frameworks
# MAGIC - Use DataValidator for quick, ad-hoc validations

# COMMAND ----------
