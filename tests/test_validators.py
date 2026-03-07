"""
Tests for the validators module
"""
import pytest
from qa_framework.validators import DataValidator


@pytest.mark.unit
class TestDataValidator:
    """Test cases for DataValidator class"""
    
    def test_validator_initialization(self, sample_dataframe):
        """Test validator can be initialized with a DataFrame"""
        validator = DataValidator(sample_dataframe)
        assert validator.df is not None
        assert len(validator.validation_results) == 0
    
    def test_check_null_values(self, sample_dataframe):
        """Test null value checking"""
        validator = DataValidator(sample_dataframe)
        null_counts = validator.check_null_values()
        
        assert "age" in null_counts
        assert null_counts["age"] == 1  # One null value in age column
        assert null_counts["id"] == 0  # No nulls in id column
    
    def test_check_null_values_specific_columns(self, sample_dataframe):
        """Test null value checking for specific columns"""
        validator = DataValidator(sample_dataframe)
        null_counts = validator.check_null_values(columns=["id", "name"])
        
        assert len(null_counts) == 2
        assert "age" not in null_counts
        assert null_counts["id"] == 0
        assert null_counts["name"] == 0
    
    def test_check_duplicates(self, duplicate_dataframe):
        """Test duplicate row detection"""
        validator = DataValidator(duplicate_dataframe)
        duplicate_count = validator.check_duplicates()
        
        assert duplicate_count == 1  # One duplicate row
    
    def test_check_no_duplicates(self, sample_dataframe):
        """Test when there are no duplicates"""
        validator = DataValidator(sample_dataframe)
        duplicate_count = validator.check_duplicates()
        
        assert duplicate_count == 0
    
    def test_check_column_exists(self, sample_dataframe):
        """Test column existence checking"""
        validator = DataValidator(sample_dataframe)
        
        assert validator.check_column_exists("id") is True
        assert validator.check_column_exists("name") is True
        assert validator.check_column_exists("nonexistent") is False
    
    def test_check_value_range(self, sample_dataframe):
        """Test value range validation"""
        validator = DataValidator(sample_dataframe)
        result = validator.check_value_range("age", min_value=0, max_value=100)
        
        assert result["violations"] == 0
        assert "column" in result
    
    def test_check_value_range_with_violations(self, sample_dataframe):
        """Test value range validation with violations"""
        validator = DataValidator(sample_dataframe)
        result = validator.check_value_range("age", min_value=30, max_value=40)
        
        # Should have violations for ages < 30 and > 40
        assert result["violations"] > 0
    
    def test_get_validation_summary(self, sample_dataframe):
        """Test validation summary generation"""
        validator = DataValidator(sample_dataframe)
        
        # Run several checks
        validator.check_null_values()
        validator.check_duplicates()
        validator.check_column_exists("id")
        
        summary = validator.get_validation_summary()
        
        assert "total_checks" in summary
        assert "passed_checks" in summary
        assert "failed_checks" in summary
        assert "pass_rate" in summary
        assert "results" in summary
        assert summary["total_checks"] > 0


@pytest.mark.integration
class TestDataValidatorIntegration:
    """Integration tests for DataValidator"""
    
    def test_full_validation_workflow(self, sample_dataframe):
        """Test complete validation workflow"""
        validator = DataValidator(sample_dataframe)
        
        # Run all validation checks
        validator.check_null_values()
        validator.check_duplicates()
        validator.check_column_exists("id")
        validator.check_column_exists("name")
        validator.check_value_range("age", min_value=0, max_value=120)
        validator.check_value_range("salary", min_value=0)
        
        # Get summary
        summary = validator.get_validation_summary()
        
        # Verify summary structure
        assert summary["total_checks"] == 10  # 4 columns null check + 1 duplicate + 2 column exists + 2 value ranges + 1 salary check = 10
        assert 0 <= summary["pass_rate"] <= 1
        assert summary["total_checks"] == summary["passed_checks"] + summary["failed_checks"]
