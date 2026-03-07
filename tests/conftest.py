"""
Pytest configuration and fixtures
"""
import pytest
from pyspark.sql import SparkSession


@pytest.fixture(scope="session")
def spark():
    """
    Create a SparkSession for testing
    """
    spark = SparkSession.builder \
        .appName("qa_framework_tests") \
        .master("local[2]") \
        .config("spark.sql.shuffle.partitions", "2") \
        .getOrCreate()
    
    yield spark
    
    spark.stop()


@pytest.fixture
def sample_dataframe(spark):
    """
    Create a sample DataFrame for testing
    """
    data = [
        (1, "Alice", 25, 50000),
        (2, "Bob", 30, 60000),
        (3, "Charlie", 35, 70000),
        (4, "David", None, 80000),  # Null value for testing
        (5, "Eve", 45, 90000),
    ]
    
    df = spark.createDataFrame(data, ["id", "name", "age", "salary"])
    return df


@pytest.fixture
def duplicate_dataframe(spark):
    """
    Create a DataFrame with duplicates for testing
    """
    data = [
        (1, "Alice", 25),
        (2, "Bob", 30),
        (1, "Alice", 25),  # Duplicate
        (3, "Charlie", 35),
    ]
    
    df = spark.createDataFrame(data, ["id", "name", "age"])
    return df
