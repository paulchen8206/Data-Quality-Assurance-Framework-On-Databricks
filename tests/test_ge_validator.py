"""
Tests for Great Expectations integration
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from qa_framework.ge_validator import GreatExpectationsValidator


@pytest.fixture
def mock_spark_df():
    """Create a mock Spark DataFrame"""
    mock_df = Mock()
    mock_df.columns = ["id", "name", "age", "amount"]
    return mock_df


@pytest.fixture
def mock_ge_context():
    """Create a mock Great Expectations DataContext"""
    with patch('great_expectations.get_context') as mock_context:
        context = MagicMock()
        mock_context.return_value = context
        
        # Setup mock expectation suite
        suite = MagicMock()
        context.get_expectation_suite.return_value = suite
        context.add_expectation_suite.return_value = suite
        
        # Setup mock validator
        validator = MagicMock()
        context.get_validator.return_value = validator
        
        # Setup mock validation results
        validation_result = MagicMock()
        validation_result.to_json_dict.return_value = {
            "success": True,
            "statistics": {
                "evaluated_expectations": 5,
                "successful_expectations": 5,
                "unsuccessful_expectations": 0,
                "success_percent": 100.0
            },
            "results": []
        }
        validator.validate.return_value = validation_result
        
        # Setup mock expectation results
        expectation_result = MagicMock()
        expectation_result.to_json_dict.return_value = {"success": True}
        
        validator.expect_table_row_count_to_be_between.return_value = expectation_result
        validator.expect_column_values_to_not_be_null.return_value = expectation_result
        validator.expect_column_values_to_be_unique.return_value = expectation_result
        validator.expect_column_values_to_be_between.return_value = expectation_result
        validator.expect_column_values_to_be_in_set.return_value = expectation_result
        validator.expect_column_values_to_match_regex.return_value = expectation_result
        validator.expect_column_mean_to_be_between.return_value = expectation_result
        validator.get_expectation_suite.return_value = suite
        
        yield context


class TestGreatExpectationsValidator:
    """Test suite for GreatExpectationsValidator"""
    
    def test_initialization(self, mock_spark_df, mock_ge_context):
        """Test validator initialization"""
        ge_validator = GreatExpectationsValidator(
            df=mock_spark_df,
            expectation_suite_name="test_suite"
        )
        
        assert ge_validator.df == mock_spark_df
        assert ge_validator.expectation_suite_name == "test_suite"
        assert ge_validator.validator is not None
    
    def test_expect_table_row_count(self, mock_spark_df, mock_ge_context):
        """Test table row count expectation"""
        ge_validator = GreatExpectationsValidator(
            df=mock_spark_df,
            expectation_suite_name="test_suite"
        )
        
        result = ge_validator.expect_table_row_count_to_be_between(
            min_value=10,
            max_value=1000
        )
        
        assert result is not None
        assert "success" in result
    
    def test_expect_column_not_null(self, mock_spark_df, mock_ge_context):
        """Test column not null expectation"""
        ge_validator = GreatExpectationsValidator(
            df=mock_spark_df,
            expectation_suite_name="test_suite"
        )
        
        result = ge_validator.expect_column_values_to_not_be_null(
            column="id",
            mostly=1.0
        )
        
        assert result is not None
        assert "success" in result
    
    def test_expect_column_unique(self, mock_spark_df, mock_ge_context):
        """Test column unique expectation"""
        ge_validator = GreatExpectationsValidator(
            df=mock_spark_df,
            expectation_suite_name="test_suite"
        )
        
        result = ge_validator.expect_column_values_to_be_unique(
            column="id",
            mostly=1.0
        )
        
        assert result is not None
        assert "success" in result
    
    def test_expect_column_values_between(self, mock_spark_df, mock_ge_context):
        """Test column values between expectation"""
        ge_validator = GreatExpectationsValidator(
            df=mock_spark_df,
            expectation_suite_name="test_suite"
        )
        
        result = ge_validator.expect_column_values_to_be_between(
            column="age",
            min_value=0,
            max_value=120,
            mostly=1.0
        )
        
        assert result is not None
        assert "success" in result
    
    def test_expect_column_values_in_set(self, mock_spark_df, mock_ge_context):
        """Test column values in set expectation"""
        ge_validator = GreatExpectationsValidator(
            df=mock_spark_df,
            expectation_suite_name="test_suite"
        )
        
        result = ge_validator.expect_column_values_to_be_in_set(
            column="name",
            value_set=["Alice", "Bob", "Charlie"],
            mostly=1.0
        )
        
        assert result is not None
        assert "success" in result
    
    def test_expect_column_values_match_regex(self, mock_spark_df, mock_ge_context):
        """Test column values match regex expectation"""
        ge_validator = GreatExpectationsValidator(
            df=mock_spark_df,
            expectation_suite_name="test_suite"
        )
        
        result = ge_validator.expect_column_values_to_match_regex(
            column="name",
            regex=r"^[A-Z][a-z]+$",
            mostly=1.0
        )
        
        assert result is not None
        assert "success" in result
    
    def test_expect_column_mean_between(self, mock_spark_df, mock_ge_context):
        """Test column mean between expectation"""
        ge_validator = GreatExpectationsValidator(
            df=mock_spark_df,
            expectation_suite_name="test_suite"
        )
        
        result = ge_validator.expect_column_mean_to_be_between(
            column="amount",
            min_value=0,
            max_value=1000
        )
        
        assert result is not None
        assert "success" in result
    
    def test_validate(self, mock_spark_df, mock_ge_context):
        """Test validation execution"""
        ge_validator = GreatExpectationsValidator(
            df=mock_spark_df,
            expectation_suite_name="test_suite"
        )
        
        results = ge_validator.validate()
        
        assert results is not None
        assert "success" in results
        assert "statistics" in results
    
    def test_get_validation_summary(self, mock_spark_df, mock_ge_context):
        """Test validation summary"""
        ge_validator = GreatExpectationsValidator(
            df=mock_spark_df,
            expectation_suite_name="test_suite"
        )
        
        summary = ge_validator.get_validation_summary()
        
        assert summary is not None
        assert "success" in summary
        assert "evaluated_expectations" in summary
        assert "successful_expectations" in summary
        assert "unsuccessful_expectations" in summary
        assert "success_percent" in summary
    
    def test_save_expectation_suite(self, mock_spark_df, mock_ge_context):
        """Test saving expectation suite"""
        ge_validator = GreatExpectationsValidator(
            df=mock_spark_df,
            expectation_suite_name="test_suite"
        )
        
        # Should not raise an exception
        ge_validator.save_expectation_suite()
        
        # Verify that context methods were called
        ge_validator.validator.get_expectation_suite.assert_called_once()
        ge_validator.context.add_or_update_expectation_suite.assert_called_once()


class TestGreatExpectationsValidatorIntegration:
    """Integration tests for Great Expectations validator"""
    
    @pytest.mark.skipif(
        True,  # Skip by default - requires Spark environment
        reason="Integration test requires Spark environment"
    )
    def test_full_validation_workflow(self):
        """Test complete validation workflow with real Spark DataFrame"""
        # This test would run in a real Spark environment
        from pyspark.sql import SparkSession
        
        spark = SparkSession.builder.master("local[1]").getOrCreate()
        
        data = [(1, "Alice", 25), (2, "Bob", 30), (3, "Charlie", 35)]
        df = spark.createDataFrame(data, ["id", "name", "age"])
        
        ge_validator = GreatExpectationsValidator(
            df=df,
            expectation_suite_name="integration_test_suite"
        )
        
        # Add expectations
        ge_validator.expect_column_values_to_not_be_null("id")
        ge_validator.expect_column_values_to_be_unique("id")
        ge_validator.expect_column_values_to_be_between("age", min_value=0, max_value=120)
        
        # Validate
        results = ge_validator.validate()
        
        assert results["success"] is True
        
        spark.stop()
