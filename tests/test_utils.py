"""
Tests for the utils module
"""
import pytest
import logging
import tempfile
from pathlib import Path
from qa_framework.utils import setup_logger, read_config, format_validation_report


@pytest.mark.unit
class TestUtils:
    """Test cases for utility functions"""
    
    def test_setup_logger(self):
        """Test logger setup"""
        logger = setup_logger("test_logger")
        
        assert isinstance(logger, logging.Logger)
        assert logger.name == "test_logger"
        assert logger.level == logging.INFO
    
    def test_setup_logger_custom_level(self):
        """Test logger setup with custom level"""
        logger = setup_logger("test_logger_debug", level=logging.DEBUG)
        
        assert logger.level == logging.DEBUG
    
    def test_read_config_valid_file(self):
        """Test reading valid config file"""
        # Create temporary config file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
            f.write("""
database:
  host: localhost
  port: 5432
validation:
  max_nulls: 0
  check_duplicates: true
""")
            config_path = f.name
        
        try:
            config = read_config(config_path)
            
            assert "database" in config
            assert "validation" in config
            assert config["database"]["host"] == "localhost"
            assert config["validation"]["max_nulls"] == 0
        finally:
            Path(config_path).unlink()
    
    def test_read_config_file_not_found(self):
        """Test reading non-existent config file"""
        with pytest.raises(FileNotFoundError):
            read_config("/nonexistent/config.yml")
    
    def test_format_validation_report(self):
        """Test validation report formatting"""
        summary = {
            "total_checks": 5,
            "passed_checks": 4,
            "failed_checks": 1,
            "pass_rate": 0.8,
            "results": [
                {"check": "null_values", "column": "id", "passed": True},
                {"check": "duplicates", "passed": False, "duplicate_count": 2},
            ]
        }
        
        report = format_validation_report(summary)
        
        assert "DATA VALIDATION REPORT" in report
        assert "Total Checks: 5" in report
        assert "Passed: 4" in report
        assert "Failed: 1" in report
        assert "80.00%" in report
        assert "✓ PASSED" in report
        assert "✗ FAILED" in report
    
    def test_format_validation_report_all_passed(self):
        """Test report formatting when all checks pass"""
        summary = {
            "total_checks": 3,
            "passed_checks": 3,
            "failed_checks": 0,
            "pass_rate": 1.0,
            "results": [
                {"check": "null_values", "passed": True},
                {"check": "duplicates", "passed": True},
                {"check": "column_exists", "passed": True},
            ]
        }
        
        report = format_validation_report(summary)
        
        assert "100.00%" in report
        assert "✗ FAILED" not in report
