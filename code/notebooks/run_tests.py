# Databricks notebook source
"""
Run QA tests in Databricks environment
"""

# COMMAND ----------

# MAGIC %pip install -r ../../requirements.txt

# COMMAND ----------

import sys
from pathlib import Path

# Add src directory to path
src_path = str(Path(".").absolute().parent)
if src_path not in sys.path:
    sys.path.insert(0, src_path)

# COMMAND ----------

from pyspark.sql import SparkSession
from qa_framework import DataValidator, setup_logger, read_config
from qa_framework.utils import format_validation_report

# Setup logger
logger = setup_logger()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Load Sample Data

# COMMAND ----------

# Create sample data for testing
spark = SparkSession.builder.getOrCreate()

sample_data = [
    (1, "Alice", 25, 50000),
    (2, "Bob", 30, 60000),
    (3, "Charlie", 35, 70000),
    (4, "David", 40, 80000),
    (5, "Eve", 45, 90000),
]

df = spark.createDataFrame(
    sample_data, 
    ["id", "name", "age", "salary"]
)

display(df)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Run Validations

# COMMAND ----------

# Initialize validator
validator = DataValidator(df)

# Run validation checks
logger.info("Starting data validation...")

# Check for null values
null_counts = validator.check_null_values()
logger.info(f"Null value check: {null_counts}")

# Check for duplicates
duplicate_count = validator.check_duplicates()
logger.info(f"Duplicate rows: {duplicate_count}")

# Check required columns exist
required_columns = ["id", "name", "age", "salary"]
for col in required_columns:
    exists = validator.check_column_exists(col)
    logger.info(f"Column '{col}' exists: {exists}")

# Check value ranges
validator.check_value_range("age", min_value=0, max_value=120)
validator.check_value_range("salary", min_value=0)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Validation Summary

# COMMAND ----------

# Get validation summary
summary = validator.get_validation_summary()

# Display formatted report
report = format_validation_report(summary)
print(report)

# COMMAND ----------

# Return summary for job tracking
dbutils.notebook.exit(summary)
