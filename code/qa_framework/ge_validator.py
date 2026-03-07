"""
Great Expectations integration for advanced data quality checks
"""
from typing import Dict, Any, List, Optional
import great_expectations as gx
from pyspark.sql import DataFrame
import logging

logger = logging.getLogger(__name__)


class GreatExpectationsValidator:
    """
    Wrapper for Great Expectations validation with PySpark DataFrames
    """
    
    def __init__(
        self, 
        df: DataFrame, 
        expectation_suite_name: str = "default_suite",
        data_context: Optional[Any] = None
    ):
        """
        Initialize Great Expectations validator
        
        Args:
            df: PySpark DataFrame to validate
            expectation_suite_name: Name of the expectation suite to use
            data_context: Optional existing DataContext. If None, creates ephemeral context.
        """
        self.df = df
        self.expectation_suite_name = expectation_suite_name
        
        # Create or use provided DataContext
        if data_context is None:
            self.context = gx.get_context()
        else:
            self.context = data_context
        
        # Convert PySpark DataFrame to Great Expectations dataset
        self.validator = self._create_validator()
    
    def _create_validator(self):
        """Create a Great Expectations validator from PySpark DataFrame"""
        try:
            # Create or get expectation suite
            try:
                suite = self.context.get_expectation_suite(self.expectation_suite_name)
            except:
                suite = self.context.add_expectation_suite(self.expectation_suite_name)
            
            # Create validator with the DataFrame
            batch_request = {
                "datasource_name": "spark_datasource",
                "data_connector_name": "default_runtime_data_connector",
                "data_asset_name": "default_asset",
                "runtime_parameters": {"batch_data": self.df},
                "batch_identifiers": {"default_identifier_name": "default_identifier"},
            }
            
            # Try to get or create datasource
            try:
                datasource = self.context.get_datasource("spark_datasource")
            except:
                datasource_config = {
                    "name": "spark_datasource",
                    "class_name": "Datasource",
                    "execution_engine": {
                        "class_name": "SparkDFExecutionEngine",
                    },
                    "data_connectors": {
                        "default_runtime_data_connector": {
                            "class_name": "RuntimeDataConnector",
                            "batch_identifiers": ["default_identifier_name"],
                        },
                    },
                }
                datasource = self.context.add_datasource(**datasource_config)
            
            validator = self.context.get_validator(
                batch_request=batch_request,
                expectation_suite_name=self.expectation_suite_name,
            )
            
            return validator
            
        except Exception as e:
            logger.error(f"Error creating validator: {e}")
            raise
    
    def expect_table_row_count_to_be_between(
        self, 
        min_value: Optional[int] = None, 
        max_value: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Expect table row count to be between min and max values
        
        Args:
            min_value: Minimum expected row count
            max_value: Maximum expected row count
            
        Returns:
            Validation result dictionary
        """
        result = self.validator.expect_table_row_count_to_be_between(
            min_value=min_value,
            max_value=max_value
        )
        return result.to_json_dict()
    
    def expect_column_values_to_not_be_null(
        self, 
        column: str,
        mostly: float = 1.0
    ) -> Dict[str, Any]:
        """
        Expect column values to not be null
        
        Args:
            column: Column name to check
            mostly: Fraction of values that must be non-null (0.0 to 1.0)
            
        Returns:
            Validation result dictionary
        """
        result = self.validator.expect_column_values_to_not_be_null(
            column=column,
            mostly=mostly
        )
        return result.to_json_dict()
    
    def expect_column_values_to_be_unique(
        self, 
        column: str,
        mostly: float = 1.0
    ) -> Dict[str, Any]:
        """
        Expect column values to be unique
        
        Args:
            column: Column name to check
            mostly: Fraction of values that must be unique (0.0 to 1.0)
            
        Returns:
            Validation result dictionary
        """
        result = self.validator.expect_column_values_to_be_unique(
            column=column,
            mostly=mostly
        )
        return result.to_json_dict()
    
    def expect_column_values_to_be_between(
        self,
        column: str,
        min_value: Optional[float] = None,
        max_value: Optional[float] = None,
        mostly: float = 1.0
    ) -> Dict[str, Any]:
        """
        Expect column values to be between min and max
        
        Args:
            column: Column name to check
            min_value: Minimum allowed value
            max_value: Maximum allowed value
            mostly: Fraction of values that must be in range (0.0 to 1.0)
            
        Returns:
            Validation result dictionary
        """
        result = self.validator.expect_column_values_to_be_between(
            column=column,
            min_value=min_value,
            max_value=max_value,
            mostly=mostly
        )
        return result.to_json_dict()
    
    def expect_column_values_to_be_in_set(
        self,
        column: str,
        value_set: List[Any],
        mostly: float = 1.0
    ) -> Dict[str, Any]:
        """
        Expect column values to be in a specified set
        
        Args:
            column: Column name to check
            value_set: List of allowed values
            mostly: Fraction of values that must be in set (0.0 to 1.0)
            
        Returns:
            Validation result dictionary
        """
        result = self.validator.expect_column_values_to_be_in_set(
            column=column,
            value_set=value_set,
            mostly=mostly
        )
        return result.to_json_dict()
    
    def expect_column_values_to_match_regex(
        self,
        column: str,
        regex: str,
        mostly: float = 1.0
    ) -> Dict[str, Any]:
        """
        Expect column values to match a regex pattern
        
        Args:
            column: Column name to check
            regex: Regular expression pattern
            mostly: Fraction of values that must match (0.0 to 1.0)
            
        Returns:
            Validation result dictionary
        """
        result = self.validator.expect_column_values_to_match_regex(
            column=column,
            regex=regex,
            mostly=mostly
        )
        return result.to_json_dict()
    
    def expect_column_mean_to_be_between(
        self,
        column: str,
        min_value: Optional[float] = None,
        max_value: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Expect column mean to be between min and max
        
        Args:
            column: Column name to check
            min_value: Minimum expected mean
            max_value: Maximum expected mean
            
        Returns:
            Validation result dictionary
        """
        result = self.validator.expect_column_mean_to_be_between(
            column=column,
            min_value=min_value,
            max_value=max_value
        )
        return result.to_json_dict()
    
    def validate(self) -> Dict[str, Any]:
        """
        Run all expectations and return validation results
        
        Returns:
            Validation results dictionary
        """
        results = self.validator.validate()
        return results.to_json_dict()
    
    def save_expectation_suite(self, filepath: Optional[str] = None) -> None:
        """
        Save the current expectation suite
        
        Args:
            filepath: Optional path to save the suite. If None, uses default location.
        """
        suite = self.validator.get_expectation_suite()
        self.context.add_or_update_expectation_suite(suite)
        logger.info(f"Saved expectation suite: {self.expectation_suite_name}")
    
    def load_expectation_suite(self, suite_name: str) -> None:
        """
        Load an existing expectation suite
        
        Args:
            suite_name: Name of the suite to load
        """
        suite = self.context.get_expectation_suite(suite_name)
        self.expectation_suite_name = suite_name
        logger.info(f"Loaded expectation suite: {suite_name}")
    
    def get_validation_summary(self) -> Dict[str, Any]:
        """
        Get a summary of validation results
        
        Returns:
            Dictionary with validation summary
        """
        results = self.validate()
        
        stats = results.get("statistics", {})
        return {
            "success": results.get("success", False),
            "evaluated_expectations": stats.get("evaluated_expectations", 0),
            "successful_expectations": stats.get("successful_expectations", 0),
            "unsuccessful_expectations": stats.get("unsuccessful_expectations", 0),
            "success_percent": stats.get("success_percent", 0),
            "results": results.get("results", [])
        }
